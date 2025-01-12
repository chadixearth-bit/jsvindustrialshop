# Generated by Django 5.1.3 on 2024-12-04 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_globalsettings_inventoryitem_description_and_more'),
        ('requisition', '0015_requisition_actual_delivery_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisitionitem',
            name='selected_source_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='source_requisition_items', to='inventory.inventoryitem'),
        ),
    ]
