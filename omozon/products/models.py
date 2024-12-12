from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
from accounts.models import SellerProfile

class Product(models.Model):
    """Base Product Model"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(
        SellerProfile, 
        on_delete=models.CASCADE, 
        related_name='products', 
        null=True,  # Allow null temporarily
        blank=True
    )
    
    class Meta:
        abstract = False  # This allows the model to be used in the database

    def __str__(self):
        return self.name

class Electronics(Product):
    """Electronics Product Subtype"""
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    warranty_months = models.IntegerField(validators=[MinValueValidator(0)])
    
    # Electronics-specific fields
    processor = models.CharField(max_length=100, null=True, blank=True)
    ram_gb = models.IntegerField(null=True, blank=True)
    storage_gb = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.brand} {self.name}"

class Clothing(Product):
    """Clothing Product Subtype"""
    SIZES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large')
    ]
    
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('U', 'Unisex')
    ]
    
    brand = models.CharField(max_length=100)
    size = models.CharField(max_length=3, choices=SIZES)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    def __str__(self):
        return f"{self.brand} {self.name} - {self.size}"

class Shoes(Product):
    """Shoes Product Subtype"""
    SHOE_TYPES = [
        ('ATHLETIC', 'Athletic'),
        ('CASUAL', 'Casual'),
        ('FORMAL', 'Formal'),
        ('SANDAL', 'Sandal'),
        ('BOOT', 'Boot')
    ]
    
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('U', 'Unisex')
    ]
    
    brand = models.CharField(max_length=100)
    shoe_type = models.CharField(max_length=10, choices=SHOE_TYPES)
    size = models.FloatField(validators=[MinValueValidator(0)])
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Additional shoe-specific fields
    arch_support = models.BooleanField(default=False)
    waterproof = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.brand} {self.name} - Size {self.size}"

class Books(Product):
    """Books Product Subtype"""
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} by {self.author}"

class Supermarket(Product):
    """Supermarket Product Subtype"""
    CATEGORIES = [
        ('FRESH', 'Fresh Produce'),
        ('DAIRY', 'Dairy'),
        ('MEAT', 'Meat'),
        ('FROZEN', 'Frozen'),
        ('PANTRY', 'Pantry Staples')
    ]
    
    category = models.CharField(max_length=10, choices=CATEGORIES)
    brand = models.CharField(max_length=100)
    expiry_date = models.DateField()
    is_organic = models.BooleanField(default=False)
    nutritional_info = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"
