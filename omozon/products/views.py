from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, ProductImage, Electronics, Clothing, Shoes, Books, Supermarket
from .forms import ProductForm, ElectronicsForm, ClothingForm, ShoesForm, BooksForm, SupermarketForm
from django.forms import modelformset_factory
from accounts.models import SELLER

from accounts.decorators import login_required_custom_user
login_required = login_required_custom_user()

@login_required
def seller_products(request):
    """
    View to display and manage seller's products
    """
    if request.user.account_type != SELLER:
        return redirect('home')
    
    products = Product.objects.filter(seller=request.user.seller_profile)
    return render(request, 'products/seller_products.html', {'products': products})

@login_required
def add_product(request):
    if request.user.account_type != SELLER:
        return redirect('home')
    
    return render(request, 'products/add_product.html')

@login_required
def add_product_dynamic(request, product_type):
    if request.user.account_type != SELLER:
        return redirect('home')
    
    if product_type == 'electronics':
        form = ElectronicsForm(request.POST or None)
    elif product_type == 'clothing':
        form = ClothingForm(request.POST or None)
    elif product_type == 'shoes':
        form = ShoesForm(request.POST or None)
    elif product_type == 'books':
        form = BooksForm(request.POST or None)
    elif product_type == 'supermarket':
        form = SupermarketForm(request.POST or None)
    else:
        return redirect('home')
    
    if request.method == 'POST':
        if form.is_valid():
            product = form.save(commit=False)
            if product.stock_quantity <= 0:
                messages.error(request, "Stock quantity must be greater than 0")
                return redirect('add_product_dynamic', product_type=product_type)
            
            product.seller = request.user.seller_profile
            product.save()
            messages.success(request, f"{product.name} product added successfully!")
            return redirect('seller_products')
        else:
            print("Form errors:", form.errors)

    template = f'products/add_product_dynamic.html'
    return render(request, template, {'form': form, 'product_type': product_type})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)

    # Use the type field to determine which form to use
    product_type = product.type

    if product_type == Product.ELECTRONICS:
        product = Electronics.objects.get(id=product_id)
        form = ElectronicsForm(request.POST or None, request.FILES or None, instance=product)
    elif product_type == Product.CLOTHING:
        product = Clothing.objects.get(id=product_id)
        form = ClothingForm(request.POST or None, request.FILES or None, instance=product)
    elif product_type == Product.SHOES:
        product = Shoes.objects.get(id=product_id)
        form = ShoesForm(request.POST or None, request.FILES or None, instance=product)
    elif product_type == Product.BOOKS:
        product = Books.objects.get(id=product_id)
        form = BooksForm(request.POST or None, request.FILES or None, instance=product)
    elif product_type == Product.SUPERMARKET:
        product = Supermarket.objects.get(id=product_id)
        form = SupermarketForm(request.POST or None, request.FILES or None, instance=product)
    else:
        return redirect('seller_products')  # Redirect if product type is invalid

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            messages.success(request, f"{product.name} product updated successfully!")
            return redirect('seller_products')
        else:
            print("Form errors:", form.errors)  # Print form errors for debugging

    return render(request, 'products/edit_product.html', {'form': form, 'product': product, 'product_type': product_type})

@login_required
def delete_product(request, product_id):
    """
    View to delete a product
    """
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('seller_products')
    
    return render(request, 'products/delete_product.html', {'product': product})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
