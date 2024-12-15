from django.db import models
from django.conf import settings
from products.models import Product
from accounts.models import CustomUser
from delivery.models import DeliveryManagerUser

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # Shipping information
    shipping_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    delivery_manager = models.ForeignKey(DeliveryManagerUser, on_delete=models.CASCADE, null=True, blank=True, related_name='managed_orders')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def calculate_total(self):
        return sum(item.get_total_price() for item in self.items.all())

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total()
        super().save(*args, **kwargs)

class CancellationReason(models.Model):
    order = models.ForeignKey(Order, related_name='cancellation_reasons', on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancellation Reason for Order {self.order.id}: {self.reason}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}" 