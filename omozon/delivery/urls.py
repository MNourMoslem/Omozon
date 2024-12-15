from django.urls import path
from .views import (
    delivery_login, pending_orders, update_order_status,
    delivery_register, delivery_logout, shipped_orders, delivered_orders
)

urlpatterns = [
    path('login/', delivery_login, name='delivery_login'),
    path('pending-orders/', pending_orders, name='pending_orders'),
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('register/', delivery_register, name='delivery_register'),
    path('logout/', delivery_logout, name='delivery_logout'),
    path('shipped-orders/', shipped_orders, name='shipped_orders'),
    path('delivered-orders/', delivered_orders, name='delivered_orders'),
] 