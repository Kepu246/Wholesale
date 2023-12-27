from django.contrib import admin
from .models import Order, Invoice, ExpenseInvoice, TaxInvoice, Inventory

admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(ExpenseInvoice)
admin.site.register(TaxInvoice)
admin.site.register(Inventory)