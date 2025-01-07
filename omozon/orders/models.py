from django.db import models
from django.conf import settings
from products.models import Product
from accounts.models import CustomUser
from delivery.models import DeliveryManagerUser

PENDING = 1
PROCESSING = 2
SHIPPED = 3
DELIVERED = 4
CANCELLED = 5

STATUES = {
    PENDING: 'Pending',
    PROCESSING: 'Processing',
    SHIPPED: 'Shipped',
    DELIVERED: 'Delivered',
    CANCELLED: 'Cancelled'
}

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    shipping_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def calculate_total(self):
        return sum(item.get_total_price() for item in self.items.all())

    def set_as_payed(self):
        self.paid = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total()
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    STATUS_CHOICES = [(key, value) for key, value in STATUES.items()]

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=PENDING)
    delivery_manager = models.ForeignKey(DeliveryManagerUser, on_delete=models.CASCADE, null=True, blank=True, related_name='managed_orders')
    created_at = models.DateTimeField(auto_now=True)

    @property
    def is_pending(self):
        return self.status == PENDING
    
    @property
    def is_processing(self):
        return self.status == PROCESSING
    
    @property
    def is_shipped(self):
        return self.status == SHIPPED
    
    @property
    def is_delivered(self):
        return self.status == DELIVERED
    
    @property
    def is_cancelled(self):
        return self.status == CANCELLED
    
    def cancel(self, reason : str =None):
        self.status = CANCELLED
        CancellationReason.objects.cerate(orderitem=self, reason=reason)
        self.save()

    def ship(self):
        self.status = SHIPPED
        self.save()

    def deliver(self):
        self.status = DELIVERED
        self.save()

    def process(self, delivery_manager):
        self.status = PROCESSING
        self.delivery_manager = delivery_manager
        self.save()

    def repend(self):
        self.status = PENDING
        self.save()

    def return_to_seller(self):
        self.repend()

    def get_total_price(self):
        return self.price * self.quantity
    
    @property
    def status_as_string(self):
        return STATUES[self.status]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}" 
    
class CancellationReason(models.Model):
    orderitem = models.ForeignKey(OrderItem, related_name='cancellation_reasons', on_delete=models.CASCADE, default=None)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancellation Reason for Order {self.order.id}: {self.reason}"