# Generated by Django 5.1.3 on 2024-11-25 15:47

import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_globalsettings_inventoryitem_description_and_more'),
        ('sales', '0002_sale_transaction_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='item',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='sale',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sold_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.inventoryitem')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sales.sale')),
            ],
        ),
    ]