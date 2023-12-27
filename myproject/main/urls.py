from django.urls import path
from .views import (list_Order, list_inventory, delete_inventory, search_orders,
                    print_document_view, check_shortage, add_inventory,
                    create_order, create_invoice, report, delete_order,
                    create_expense_invoice, create_tax_invoice, search_inventory)


urlpatterns = [
    path('order_list/', list_Order, name='list_Order'),
    path('inventory_list/', list_inventory, name='List_inventory'),
    path('inventory_add/', add_inventory, name='add_inventory'),
    path('search_orders/', search_orders, name='search_orders'),
    path('search_inventory/', search_inventory, name='search_inventory'),
    path('check_shortage/', check_shortage, name='check_shortage'),
    path('delete_inventory/<uuid:inventor_id>/', delete_inventory, name='delete_inventory'),
    path('print_document/<uuid:order_id>/', print_document_view, name='print_document'),
    path('create_order/', create_order, name='create_order'),
    path('create_invoice/<uuid:order_id>/', create_invoice, name='create_invoice'),
    path('create_expense_invoice/<int:invoice_id>/', create_expense_invoice, name='create_expense_invoice'),
    path('create_tax_invoice/<int:expense_invoice_id>/', create_tax_invoice, name='create_tax_invoice'),
    path('report/', report, name='report'),
    path('delete_order/<uuid:order_id>/', delete_order, name='delete_order'),
]
