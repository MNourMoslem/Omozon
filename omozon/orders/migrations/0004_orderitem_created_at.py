# Generated by Django 5.1.2 on 2024-12-31 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_cancellationreason_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
