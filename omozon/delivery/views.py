from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order  # Adjust the import based on your project structure

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shipped_orders')  # Redirect to shipped orders page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'delivery/custom_login.html')

@login_required
def shipped_orders(request):
    orders = Order.objects.filter(status='SHIPPED').order_by('-created_at')
    return render(request, 'delivery/shipped_orders.html', {'orders': orders})

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deliver':
            order.status = 'DELIVERED'
            messages.success(request, "Order has been delivered.")
        elif action == 'cancel':
            order.status = 'CANCELLED'
            messages.success(request, "Order has been cancelled.")
        order.save()
        return redirect('shipped_orders')

    return render(request, 'delivery/update_order_status.html', {'order': order})
