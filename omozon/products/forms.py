from django import forms
from .models import Product, ProductImage, Electronics, Clothing, Shoes, Books, Supermarket

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 
            'description', 
            'price', 
            'image', 
            'stock_quantity'
        ] 

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image'] 

class ElectronicsForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Electronics
        fields = ProductForm.Meta.fields + ['brand', 'model_number', 'warranty_months', 'processor', 'ram_gb', 'storage_gb']

class ClothingForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Clothing
        fields = ProductForm.Meta.fields + ['brand', 'size', 'color', 'material']

class ShoesForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Shoes
        fields = ProductForm.Meta.fields + ['brand', 'size', 'color', 'material']

class BooksForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Books
        fields = ProductForm.Meta.fields + ['author', 'publisher', 'publication_year']

class SupermarketForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Supermarket
        fields = ProductForm.Meta.fields + ['category', 'expiry_date']  
