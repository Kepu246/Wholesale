from django.db import models
import uuid


class Inventory(models.Model):
    inventory_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    quantity = models.IntegerField(null=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    entry_date = models.DateField(null=False, auto_now_add=True)

    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
        if self.quantity <= 0:
            self.quantity = 0
        self.save()

    def __str__(self):
        return (
            f"ID: {self.inventory_id}"
            f"Name: {self.name}, Quantity: {self.quantity}, Cost: {self.cost}, "
            f"EntryDate: {self.entry_date}, Subtotal: {self.subtotal}"
        )


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, related_name='orders')
    order_date = models.DateField(null=False, auto_now_add=True, editable=False)
    name_client = models.CharField(max_length=255, null=False)
    quantity = models.IntegerField(null=False, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"ID: {self.order_id}, Name: {self.name_client}"

    def get_product_cost(self):
        return self.product.cost

    def create_invoice(self, confirmed_date, payment_method):
        invoice = Invoice.objects.create(
            order=self,
            confirmed_date=confirmed_date,
            payment_method=payment_method
        )
        return invoice


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="invoices")
    confirmed_date = models.DateField(auto_now_add=True, null=False)
    payment_method = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"ID: {self.invoice_id}, Order: {self.order}, Confirmed_date: {self.confirmed_date}"


class ExpenseInvoice(models.Model):
    expense_invoice_id = models.AutoField(primary_key=True)
    invoice = models.OneToOneField('Invoice', on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"ID: {self.expense_invoice_id}, Invoice: {self.invoice}, Issue date: {self.issue_date}"

    def create_tax_invoice(self):
        tax_invoice = TaxInvoice.objects.create(
            expense_invoice=self
        )
        return tax_invoice


class TaxInvoice(models.Model):
    tax_invoice_id = models.AutoField(primary_key=True)
    expense_invoice = models.OneToOneField(ExpenseInvoice, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"ID: {self.tax_invoice_id}, Expense invoice: {self.expense_invoice}, Issue date: {self.issue_date}"

