from django import forms
from .models import Order, Invoice, Inventory, ExpenseInvoice, TaxInvoice


class OrderCreationForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Inventory.objects.all(), required=True, label='Product')

    class Meta:
        model = Order
        fields = ['name_client', 'quantity', 'product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Inventory.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product: Inventory = cleaned_data.get('product')

        if quantity is not None and product is not None:
            cleaned_data['unit_price'] = product.cost
            subtotal = quantity * product.cost
            cleaned_data['subtotal'] = subtotal

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subtotal = self.cleaned_data.get('subtotal', instance.quantity * instance.product.cost)
        instance.unit_price = self.cleaned_data.get('unit_price', instance.product.cost)

        if commit:
            instance.save()
        return instance


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['payment_method']


class ExpenseInvoiceForm(forms.ModelForm):
    class Meta:
        model = ExpenseInvoice
        fields = ['description']


class TaxInvoiceForm(forms.ModelForm):
    class Meta:
        model = TaxInvoice
        fields = ['description']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'quantity', 'cost']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity', 0)
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subtotal = instance.quantity * instance.cost
        if commit:
            instance.save()
        return instance


class DeleteInventoryForm(forms.Form):
    items_to_delete = forms.ModelMultipleChoiceField(
        queryset=Inventory.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
