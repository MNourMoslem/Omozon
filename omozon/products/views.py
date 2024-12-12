from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def seller_products(request):
    """
    View to display and manage seller's products
    """
    if request.user.account_type != 'SELLER':
        return redirect('home')
    
    products = Product.objects.filter(seller=request.user.seller_profile)
    return render(request, 'products/seller_products.html', {'products': products})

@login_required
def add_product(request):
    """
    View to add a new product for a seller
    """
    if request.user.account_type != 'SELLER':
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            
            # Update seller's product count
            request.user.seller_profile.update_product_count()
            
            return redirect('seller_products')
    else:
        form = ProductForm()
    
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    """
    View to edit an existing product
    """
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('seller_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

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
