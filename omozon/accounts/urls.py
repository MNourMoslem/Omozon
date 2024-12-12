from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_user, register_seller, register_buyer, edit_profile
from orders import views as order_views

urlpatterns = [
    path('register/', views.register_buyer, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('switch-to-seller/', views.switch_to_seller, name='switch_to_seller'),
    path('orders/', order_views.order_list, name='order_list'),
    path('orders/<int:order_id>/', order_views.order_detail, name='order_detail'),
    path('register/buyer/', register_buyer, name='register_buyer'),
    path('register/seller/', register_seller, name='register_seller'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]