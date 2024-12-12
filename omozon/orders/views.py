from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        # Get shipping address from form
        shipping_address = request.POST.get('shipping_address')
        
        if not shipping_address:
            messages.error(request, "Please provide a shipping address")
            return render(request, 'orders/checkout.html', {'cart': cart})
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            total_price=cart.get_total_price()
        )
        
        # Transfer cart items to order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Clear the cart
        cart.items.all().delete()
        
        messages.success(request, "Order placed successfully!")
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order}) 