# Generated by Django 5.1.3 on 2024-12-12 13:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_remove_sellerprofile_rating_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="buyerprofile",
            name="default_shipping_address",
        ),
        migrations.RemoveField(
            model_name="buyerprofile",
            name="total_purchases",
        ),
        migrations.AddField(
            model_name="customuser",
            name="default_shipping_address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="total_purchases",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
