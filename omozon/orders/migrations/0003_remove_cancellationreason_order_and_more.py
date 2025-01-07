# Generated by Django 5.1.2 on 2024-12-31 13:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
        ('orders', '0002_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cancellationreason',
            name='order',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_manager',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='cancellationreason',
            name='orderitem',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='cancellation_reasons', to='orders.orderitem'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='delivery_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='managed_orders', to='delivery.deliverymanageruser'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Pending'), (2, 'Processing'), (3, 'Shipped'), (4, 'Delivered'), (5, 'Cancelled')], default=1),
        ),
    ]
