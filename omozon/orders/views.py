from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem, CancellationReason
from .forms import OrderForm
from django.db.models import F
from django.core.mail import send_mail
from django.conf import settings
from accounts.decorators import login_required_custom_user

login_required = login_required_custom_user()

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
            if cart_item.quantity > cart_item.product.stock_quantity:
                messages.error(request, "Product is out of stock")
                return redirect('view_cart')

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
            subject = "New Order Received"
            message = f"You have received a new order: Order ID {order.id}."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.seller.email])
            return redirect('order_success')  # Redirect to a success page
    else:
        form = OrderForm(user=request.user)  # Pass the user to pre-fill the form

    return render(request, 'orders/create_order.html', {'form': form}) 

@login_required
def seller_orders(request):
    """View for sellers to see their orders."""
    if request.user.account_type != 'SELLER':
        return redirect('home')  # Redirect to home if the user is not a seller

    orders = Order.objects.filter(user=request.user)  # Assuming the seller is the user
    return render(request, 'orders/seller_orders.html', {'orders': orders})

@login_required
def update_order_status(request, order_id):
    """View for sellers to cancel the order status."""
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        cancellation_reason = request.POST.get('cancellation_reason', '')

        if order.status == 'SHIPPED':
            messages.error(request, "You cannot cancel an order that has already been shipped.")
        else:
            order.status = 'CANCELLED'
            CancellationReason.objects.create(order=order, reason=cancellation_reason)
            messages.success(request, "Order has been cancelled.")
            order.products.all().update(stock_quantity=F('stock_quantity') + order.products.all().count())

        order.save()
        return redirect('seller_orders')

    cancellation_reasons = order.cancellation_reasons.all()  # Get cancellation reasons for the order
    return render(request, 'orders/update_order_status.html', {'order': order, 'cancellation_reasons': cancellation_reasons})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'PENDING':
        messages.error(request, "You cannot delete an order that is not pending")
        return redirect('order_list')
    
    order.delete()
    return redirect('order_list')
