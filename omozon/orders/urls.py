from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('list/', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create-order/', views.create_order, name='create_order'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('seller/orders/update/<int:orderitem_id>/', views.update_order_status, name='update_order_status'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
]