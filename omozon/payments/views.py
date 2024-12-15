import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order, OrderItem
from delivery.models import DeliveryManagerUser
from .models import Payment
from .forms import PaymentForm

from accounts.decorators import login_required_custom_user
login_required = login_required_custom_user()

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def _decrease_product_stock(order):
    for item in OrderItem.objects.filter(order=order):
        product = item.product
        product.stock_quantity -= item.quantity
        product.save()

def _get_order_delivery_manager(order):
    import random
    delivery_managers = DeliveryManagerUser.objects.all()
    return random.choice(delivery_managers)

@login_required
def checkout_view(request, order_id):
    """
    Checkout page for a specific order
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Create Stripe Checkout Session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(order.total_price * 100),  # Convert to cents
                    'product_data': {
                        'name': f'Order #{order.id}',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payments/success/{order.id}/'),
            cancel_url=request.build_absolute_uri(f'/payments/cancel/{order.id}/'),
            client_reference_id=str(order.id)
        )

        return render(request, 'payments/checkout.html', {
            'order': order,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'checkout_session_id': checkout_session.id
        })
    except Exception as e:
        messages.error(request, f"Error creating checkout session: {str(e)}")
        return redirect('order_detail', order_id=order.id)

@login_required
def payment_success(request, order_id):
    """
    Handle successful payment
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Create payment record
    Payment.objects.create(
        user=request.user,
        order=order,
        amount=order.total_price,
        status='COMPLETED'
    )
    
    # Update order status
    order.status = 'PROCESSING'
    order.save()
    
    messages.success(request, "Payment successful! Your order is being processed.")
    return redirect('order_detail', order_id=order.id)

@login_required
def payment_cancel(request, order_id):
    """
    Handle payment cancellation
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    messages.warning(request, "Payment was cancelled. Please try again.")
    return redirect('order_detail', order_id=order.id)

@csrf_exempt
def stripe_webhook(request):
    """
    Handle Stripe webhooks
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle specific event types
    if event.type == 'checkout.session.completed':
        session = event.data.object
        order_id = session.client_reference_id
        
        try:
            order = Order.objects.get(id=order_id)
            Payment.objects.create(
                user=order.user,
                order=order,
                stripe_charge_id=session.payment_intent,
                amount=order.total_price,
                status='COMPLETED'
            )
            order.status = 'PROCESSING'
            order.save()
        except Order.DoesNotExist:
            pass
    
    return HttpResponse(status=200)

@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Simulate payment processing
            card_number = form.cleaned_data['card_number']
            expiration_date = form.cleaned_data['expiration_date']
            cvv = form.cleaned_data['cvv']

            # Here you can add logic to validate the card details
            # For this example, we'll assume the payment is always successful
            # payment = Payment.objects.create(
            #     user=request.user,
            #     order=order,
            #     amount=order.total_price,
            #     status='COMPLETED'
            # )

            # Update order status
            order.status = 'PROCESSING'
            _decrease_product_stock(order)
            order.delivery_manager = _get_order_delivery_manager(order)
            order.save()

            messages.success(request, "Payment successful! Your order is being processed.")
            return redirect('order_detail', order_id=order.id)
    else:
        form = PaymentForm()

    return render(request, 'payments/payment.html', {'form': form, 'order': order})