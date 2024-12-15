from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .forms import DeliveryLoginForm, DeliveryRegisterForm
from .models import DeliveryManagerUser
from django.http import HttpResponseForbidden
from accounts.models import DELIVERY_MANAGER

def login_required_delivery_manager():
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.account_type == DELIVERY_MANAGER:
                return view_func(request, *args, **kwargs)
            print(request.user.account_type)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator

def _get_delivery_manager_orders(request, **kwargs):
    user = DeliveryManagerUser.objects.get(user=request.user)
    orders = Order.objects.filter(delivery_manager=user, **kwargs)
    return orders

def delivery_login(request):
    if request.method == 'POST':
        form = DeliveryLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pending_orders')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = DeliveryLoginForm()
    return render(request, 'delivery/delivery_login.html', {'form': form})

def delivery_register(request):
    if request.method == 'POST':
        form = DeliveryRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('delivery_login')
        else:
            print(form.errors)  # Debugging line to see what errors are present
    else:
        form = DeliveryRegisterForm()
    return render(request, 'delivery/delivery_register.html', {'form': form})

@login_required_delivery_manager()
def delivery_logout(request):
    logout(request)
    return redirect('delivery_login')

@login_required_delivery_manager()
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status != 'PENDING' or order.status != 'SHIPPED':
        messages.error(request, "Order is not in a valid status to be updated.")
        return redirect('delivered_orders')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deliver':
            order.status = 'DELIVERED'
            messages.success(request, "Order has been delivered.")
        elif action == 'ship':
            order.status = 'SHIPPED'
            messages.success(request, "Order has been shipped.")
        elif action == 'cancel':
            order.status = 'CANCELLED'
            messages.success(request, "Order has been cancelled.")
        else:
            messages.error(request, "Invalid action.")
        order.save()
        return redirect('pending_orders')

    return render(request, 'delivery/update_order_status.html', {'order': order})

@login_required_delivery_manager()
def pending_orders(request):
    orders = _get_delivery_manager_orders(request, status='PROCESSING').order_by('-created_at')
    return render(request, 'delivery/delivery_orders.html', {'orders': orders})

@login_required_delivery_manager()
def shipped_orders(request):
    orders = _get_delivery_manager_orders(request, status='SHIPPED').order_by('-created_at')
    return render(request, 'delivery/delivery_orders.html', {'orders': orders})

@login_required_delivery_manager()
def delivered_orders(request):
    orders = _get_delivery_manager_orders(request, status='DELIVERED').order_by('-created_at')
    return render(request, 'delivery/delivery_orders.html', {'orders': orders})
