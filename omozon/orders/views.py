from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from .forms import OrderForm

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
    else:
        # Pre-fill the form with the user's default shipping address
        default_shipping_address = request.user.default_shipping_address
        return render(request, 'orders/checkout.html', {
            'cart': cart,
            'default_shipping_address': default_shipping_address
        })

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)  # Pass the user to the form
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Set the user for the order
            order.save()
            return redirect('order_success')  # Redirect to a success page
    else:
        form = OrderForm(user=request.user)  # Pass the user to pre-fill the form

    return render(request, 'orders/create_order.html', {'form': form}) 