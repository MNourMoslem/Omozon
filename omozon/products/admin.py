from django.contrib import admin
from .models import Product, Electronics, Clothing, Shoes, Books, Supermarket

# Register each model with the admin site
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Electronics)
class ElectronicsAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'model_number', 'price')
    list_filter = ('brand',)

@admin.register(Clothing)
class ClothingAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'size', 'color', 'price')
    list_filter = ('brand', 'size', 'color')

@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'shoe_type', 'size', 'color', 'gender')
    list_filter = ('brand', 'shoe_type', 'gender')

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'isbn', 'publication_year', 'price')
    list_filter = ('genre', 'publication_year')

@admin.register(Supermarket)
class SupermarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'expiry_date', 'is_organic')
    list_filter = ('category', 'is_organic')
