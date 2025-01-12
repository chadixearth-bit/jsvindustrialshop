# Generated by Django 5.0.9 on 2024-12-18 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("requisition", "0024_remove_delivery_delivery_personnel_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="delivery",
            name="delivery_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="delivery_images/"
            ),
        ),
        migrations.AlterField(
            model_name="delivery",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending_delivery", "Pending Delivery"),
                    ("in_delivery", "In Delivery"),
                    ("pending_manager", "Pending Manager Confirmation"),
                    ("pending_admin", "Pending Admin Confirmation"),
                    ("received", "Received"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending_delivery",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="deliveryitem",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending_delivery", "Pending Delivery"),
                    ("in_delivery", "In Delivery"),
                    ("pending_manager", "Pending Manager Confirmation"),
                    ("pending_admin", "Pending Admin Confirmation"),
                    ("received", "Received"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending_delivery",
                max_length=20,
            ),
        ),
    ]