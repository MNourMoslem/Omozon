# Generated by Django 5.1.3 on 2024-12-12 07:41

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Books",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products.product",
                    ),
                ),
                ("author", models.CharField(max_length=255)),
                ("isbn", models.CharField(max_length=13, unique=True)),
                ("publisher", models.CharField(max_length=255)),
                ("publication_year", models.IntegerField()),
                ("genre", models.CharField(max_length=100)),
            ],
            bases=("products.product",),
        ),
        migrations.CreateModel(
            name="Clothing",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products.product",
                    ),
                ),
                ("brand", models.CharField(max_length=100)),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("XS", "Extra Small"),
                            ("S", "Small"),
                            ("M", "Medium"),
                            ("L", "Large"),
                            ("XL", "Extra Large"),
                            ("XXL", "Double Extra Large"),
                        ],
                        max_length=3,
                    ),
                ),
                ("color", models.CharField(max_length=50)),
                ("material", models.CharField(max_length=100)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Men"), ("W", "Women"), ("U", "Unisex")],
                        max_length=1,
                    ),
                ),
            ],
            bases=("products.product",),
        ),
        migrations.CreateModel(
            name="Electronics",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products.product",
                    ),
                ),
                ("brand", models.CharField(max_length=100)),
                ("model_number", models.CharField(max_length=100)),
                (
                    "warranty_months",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("processor", models.CharField(blank=True, max_length=100, null=True)),
                ("ram_gb", models.IntegerField(blank=True, null=True)),
                ("storage_gb", models.IntegerField(blank=True, null=True)),
            ],
            bases=("products.product",),
        ),
        migrations.CreateModel(
            name="Shoes",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products.product",
                    ),
                ),
                ("brand", models.CharField(max_length=100)),
                (
                    "shoe_type",
                    models.CharField(
                        choices=[
                            ("ATHLETIC", "Athletic"),
                            ("CASUAL", "Casual"),
                            ("FORMAL", "Formal"),
                            ("SANDAL", "Sandal"),
                            ("BOOT", "Boot"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "size",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("color", models.CharField(max_length=50)),
                ("material", models.CharField(max_length=100)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Men"), ("W", "Women"), ("U", "Unisex")],
                        max_length=1,
                    ),
                ),
                ("arch_support", models.BooleanField(default=False)),
                ("waterproof", models.BooleanField(default=False)),
            ],
            bases=("products.product",),
        ),
        migrations.CreateModel(
            name="Supermarket",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products.product",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("FRESH", "Fresh Produce"),
                            ("DAIRY", "Dairy"),
                            ("MEAT", "Meat"),
                            ("FROZEN", "Frozen"),
                            ("PANTRY", "Pantry Staples"),
                        ],
                        max_length=10,
                    ),
                ),
                ("brand", models.CharField(max_length=100)),
                ("expiry_date", models.DateField()),
                ("is_organic", models.BooleanField(default=False)),
                ("nutritional_info", models.TextField(blank=True, null=True)),
            ],
            bases=("products.product",),
        ),
        migrations.AddField(
            model_name="product",
            name="stock_quantity",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
    ]
