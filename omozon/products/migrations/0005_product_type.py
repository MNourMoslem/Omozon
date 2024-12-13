# Generated by Django 5.1.3 on 2024-12-12 17:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_productimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="type",
            field=models.CharField(
                choices=[
                    ("electronics", "Electronics"),
                    ("clothing", "Clothing"),
                    ("shoes", "Shoes"),
                    ("books", "Books"),
                    ("supermarket", "Supermarket"),
                ],
                default="electronics",
                max_length=20,
            ),
        ),
    ]
