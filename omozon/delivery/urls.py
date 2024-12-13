from django.urls import path
from .views import custom_login, shipped_orders, update_order_status

urlpatterns = [
    path('login/', custom_login, name='custom_login'),
    path('shipped-orders/', shipped_orders, name='shipped_orders'),
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
] 