# Generated by Django 5.0 on 2023-12-24 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_invoices_order_alter_orders_order_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExpenseInvoices',
            new_name='ExpenseInvoice',
        ),
        migrations.RenameModel(
            old_name='Invoices',
            new_name='Invoice',
        ),
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
        migrations.RenameModel(
            old_name='TaxInvoices',
            new_name='TaxInvoice',
        ),
    ]
