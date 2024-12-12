from django.shortcuts import render
from products.models import Product

def home_view(request):
    featured_products = Product.objects.all()[:6]  # Get first 6 products
    return render(request, 'home.html', {
        'featured_products': featured_products
    }) 