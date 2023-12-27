# Generated by Django 5.0 on 2023-12-25 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_inventory_inventory_id_alter_order_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseinvoice',
            name='invoice',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.invoice'),
        ),
        migrations.AlterField(
            model_name='taxinvoice',
            name='expense_invoice',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.expenseinvoice'),
        ),
        migrations.AlterField(
            model_name='warnings',
            name='expense_invoice',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.expenseinvoice'),
        ),
    ]
