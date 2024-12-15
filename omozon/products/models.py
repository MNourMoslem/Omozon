from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator

class Product(models.Model):
    """Base Product Model"""
    ELECTRONICS = 1
    CLOTHING = 2
    SHOES = 3
    BOOKS = 4
    SUPERMARKET = 5

    PRODUCT_TYPES = [
        (ELECTRONICS, 'Electronics'),
        (CLOTHING, 'Clothing'),
        (SHOES, 'Shoes'),
        (BOOKS, 'Books'),
        (SUPERMARKET, 'Supermarket'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/products', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(
        "accounts.SellerUser", 
        on_delete=models.CASCADE, 
        related_name='products', 
        null=True,  
        blank=True
    )
    type = models.IntegerField(choices=PRODUCT_TYPES)

    class Meta:
        abstract = False  # This allows the model to be used in the database

    def __str__(self):
        return self.name

    @property
    def type2str(self):
        return self.PRODUCT_TYPES[self.type - 1][1]

class Electronics(Product):
    """Electronics Product Subtype"""
    
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    warranty_months = models.IntegerField(validators=[MinValueValidator(0)])
    
    # Electronics-specific fields
    processor = models.CharField(max_length=100, null=True, blank=True)
    ram_gb = models.IntegerField(null=True, blank=True)
    storage_gb = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.type = Product.ELECTRONICS
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.name}"

class Clothing(Product):
    """Clothing Product Subtype"""
    type = Product.CLOTHING  # Set the type for Clothing
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
    

    def save(self, *args, **kwargs):
        self.type = Product.CLOTHING
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.name} - {self.size}"

class Shoes(Product):
    """Shoes Product Subtype"""
    type = Product.SHOES  # Set the type for Shoes
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
    

    def save(self, *args, **kwargs):
        self.type = Product.SHOES
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.name} - Size {self.size}"

class Books(Product):
    """Books Product Subtype"""
    type = Product.BOOKS  # Set the type for Books
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    

    def save(self, *args, **kwargs):
        self.type = Product.BOOKS
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} by {self.author}"

class Supermarket(Product):
    """Supermarket Product Subtype"""
    type = Product.SUPERMARKET  # Set the type for Supermarket
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
    

    def save(self, *args, **kwargs):
        self.type = Product.SUPERMARKET
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
