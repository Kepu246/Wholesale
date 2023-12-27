from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from .models import Order, ExpenseInvoice, Inventory, Invoice
from .forms import OrderCreationForm, InventoryForm, ExpenseInvoiceForm, TaxInvoiceForm, InvoiceForm
from reportlab.pdfgen import canvas
from io import BytesIO


def list_Order(request):
    orders_invoices = Order.objects.prefetch_related('invoices').all()
    return render(request, 'main/List_Order.html', {'orders_invoices': orders_invoices})


def list_inventory(request):
    inventory = Inventory.objects.all()

    return render(request, 'main/List_inventory.html', {"inventory": inventory})


def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            new_inventory = form.save()
            data = {
                'name': new_inventory.name,
                'quantity': new_inventory.quantity,
                'cost': new_inventory.cost,
                'subtotal': new_inventory.subtotal,
                'entry_date': new_inventory.entry_date.strftime('%Y-%m-%d'),
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid form data.'}, status=400)
    else:
        form = InventoryForm()

    return render(request, '', {'form': form})


def delete_inventory(request, inventor_id):
    try:
        inventory = Inventory.objects.get(inventory_id=inventor_id)
        inventory.delete()
        return JsonResponse({'success': True})
    except Inventory.DoesNotExist:
        return JsonResponse({'error': 'Inventory not found'}, status=404)


def print_document_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    invoices = order.invoices.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="document_{order_id}.pdf"'

    buffer = BytesIO()

    try:
        p = canvas.Canvas(buffer)
        font_name = 'Helvetica'
        font_size = 12
        x_position = 100
        y_position = 780
        p.setFont(font_name, font_size + 2)
        p.drawString(x_position, y_position, "Order:")
        y_position -= 20
        p.setFont(font_name, font_size)
        p.drawString(x_position, y_position, f"Order ID: {order.order_id}")
        y_position -= 20
        p.drawString(x_position, y_position, f"Order Date: {order.order_date}")
        y_position -= 20
        p.drawString(x_position, y_position, f"Client Name: {order.name_client}")
        y_position -= 40
        p.setFont(font_name, font_size + 2)
        p.drawString(x_position, y_position, "Invoices:")
        y_position -= 20
        if order.product:
            p.drawString(x_position, y_position, f"Product Name: {order.product.name}")
            y_position -= 20
        for invoice in invoices:
            p.setFont(font_name, font_size)
            p.drawString(x_position, y_position, f"Confirmed Date: {invoice.confirmed_date}")
            y_position -= 20
            p.drawString(x_position, y_position, f"Payment Method: {invoice.payment_method}")
            y_position -= 20

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

    return response


def check_shortage(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        quantity = request.GET.get('quantity')
        product = get_object_or_404(Inventory, pk=product_id)
        if product.quantity >= int(quantity):
            message = f"Available: {product.quantity}"
            shortage_quantity = 0
        else:
            shortage_quantity = int(quantity) - product.quantity
            message = f"Shortage: {shortage_quantity}"

        return JsonResponse({'message': message, 'shortage': shortage_quantity})


def create_order(request):
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if form.cleaned_data['product']:
                order.product = form.cleaned_data['product']
                order.unit_price = order.product.cost
                order.subtotal = order.quantity * order.unit_price
                order.save()
                order.product.update_quantity(order.product.quantity - order.quantity)
                if order.product.quantity == 0:
                    order.product.delete()

                return redirect('create_invoice', order_id=order.order_id)
            else:
                messages.error(request, "Product is required.")
                return redirect('list_Order')
    else:
        form = OrderCreationForm()

    return render(request, 'main/create_order.html', {'form': form})


def create_invoice(request, order_id):
    order = Order.objects.get(order_id=order_id)
    subtotal = order.subtotal

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.order = order
            invoice.save()
            return redirect('create_expense_invoice', invoice_id=invoice.invoice_id)
    else:
        form = InvoiceForm()

    return render(request, 'main/create_invoice.html', {'form': form, 'order': order, 'subtotal': subtotal})


def create_expense_invoice(request, invoice_id):
    invoice = Invoice.objects.get(invoice_id=invoice_id)
    if request.method == 'POST':
        form = ExpenseInvoiceForm(request.POST)
        if form.is_valid():
            expense_invoice = form.save(commit=False)
            expense_invoice.invoice = invoice
            expense_invoice.save()
            return redirect('create_tax_invoice', expense_invoice_id=expense_invoice.expense_invoice_id)
    else:
        form = ExpenseInvoiceForm()
    return render(request, 'main/create_expense_invoice.html', {'form': form, 'invoice': invoice})


def create_tax_invoice(request, expense_invoice_id):
    expense_invoice = ExpenseInvoice.objects.get(expense_invoice_id=expense_invoice_id)
    if request.method == 'POST':
        form = TaxInvoiceForm(request.POST)
        if form.is_valid():
            tax_invoice = form.save(commit=False)
            tax_invoice.expense_invoice = expense_invoice
            tax_invoice.save()
            return redirect('list_Order')
    else:
        form = TaxInvoiceForm()
    return render(request, 'main/create_tax_invoice.html', {'form': form, 'expense_invoice': expense_invoice})


def report(request):
    items_to_delete = Inventory.objects.filter(quantity__lte=0)

    items_to_delete.delete()

    all_items = Inventory.objects.all()

    total_sum = sum(item.subtotal for item in all_items)

    context = {
        'all_items': all_items,
        'total_sum': total_sum,
    }

    return render(request, 'main/report.html', context)


def delete_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('list_Order')

    return render(request, '', {'order': order})


def search_orders(request):
    search_id = request.GET.get('search_id', '')

    if search_id:
        orders_invoices = Order.objects.filter(order_id__icontains=search_id)
    else:
        orders_invoices = Order.objects.all()

    data = render_to_string('main/List_Order.html', {'orders_invoices': orders_invoices})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'html': data})
    else:
        return render(request, 'main/List_Order.html', {'orders_invoices': orders_invoices})


def search_inventory(request):
    search_name = request.GET.get('name', '')
    if search_name:
        results = Inventory.objects.filter(name__icontains=search_name)
        inventory_list = [
            {
                'inventory_id': str(inventory.inventory_id),
                'name': inventory.name,
                'quantity': inventory.quantity,
                'cost': str(inventory.cost),
                'subtotal': str(inventory.subtotal),
                'entry_date': inventory.entry_date.strftime('%Y-%m-%d'),
            }
            for inventory in results
        ]

        return JsonResponse(inventory_list, safe=False)