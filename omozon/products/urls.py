from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('seller/products/', views.seller_products, name='seller_products'),
    path('seller/products/add/', views.add_product, name='add_product'),
    path('seller/products/add/<str:product_type>/', views.add_product_dynamic, name='add_product_dynamic'),
    path('seller/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]