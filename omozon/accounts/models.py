from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings

BUYER = 1
SELLER = 2
DELIVERY_MANAGER = 3

class CustomUser(AbstractUser):
    """
    Custom User model that supports both buyers and sellers
    """

    ACCOUNT_TYPE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
        (DELIVERY_MANAGER, 'Delivery Manager')
    ]

    account_type = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES, default=BUYER)
    
    # Phone number validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True
    )

    # New fields
    default_shipping_address = models.TextField(blank=True, null=True)
    total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
    )

    def __str__(self):
        return self.username

    @property
    def is_delivery_manager(self):
        return self.account_type == DELIVERY_MANAGER

    @property
    def is_seller(self):
        return self.account_type == SELLER

    @property
    def is_buyer(self):
        return self.account_type == BUYER

    @property
    def is_custom_user(self):
        return self.is_buyer or self.is_seller

    def can_become_seller(self):
        """
        Check if user can switch to seller account
        You can add additional logic here if needed
        """
        return self.is_buyer()

    def switch_to_seller(self, **kwargs):
        """
        Switch user account type to seller`
        """
        if self.can_become_seller():
            self.account_type = SELLER
            self.save()
            
            # Create seller profile if not exists
            SellerUser.objects.get_or_create(user=self, **kwargs)
            BuyerUser.objects.filter(user=self).delete()
            return True
        return False

class SellerUser(models.Model):
    """
    Additional profile information for sellers
    """
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='seller_profile'
    )
    
    business_name = models.CharField(max_length=255, blank=True, default='')
    business_description = models.TextField(blank=True, default='')
    
    # Business address
    address = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    postal_code = models.CharField(max_length=20, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    
    # Seller performance metrics
    total_products = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seller_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)

    def update_product_count(self):
        """
        Update total number of products for this seller
        """
        self.total_products = self.products.count()
        self.save()

    def save(self, *args, **kwargs):
        self.account_type = SELLER
        super().save(*args, **kwargs)

    def __str__(self):
        return self.business_name or f"Seller {self.user.username}"

class BuyerUser(models.Model):
    """
    Additional profile information for buyers
    """
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='buyer_profile'
    )

    def save(self, *args, **kwargs):
        self.account_type = BUYER
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Buyer: {self.user.username}"
