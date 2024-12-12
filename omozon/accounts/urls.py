from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_user

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('switch-to-seller/', views.switch_to_seller, name='switch_to_seller'),
]