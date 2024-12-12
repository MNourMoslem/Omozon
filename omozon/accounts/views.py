from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import BuyerProfile, SellerProfile

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create profile based on account type
            if user.account_type == 'BUYER':
                BuyerProfile.objects.create(user=user)
            elif user.account_type == 'SELLER':
                SellerProfile.objects.create(user=user)
            
            # Authenticate and login
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.user.account_type == 'BUYER':
        return render(request, 'accounts/buyer_profile.html')
    elif request.user.account_type == 'SELLER':
        return render(request, 'accounts/seller_profile.html')
    else:
        return redirect('home')

@login_required
def switch_to_seller(request):
    if request.method == 'POST':
        if request.user.can_become_seller():
            request.user.switch_to_seller()
            messages.success(request, 'You have successfully switched to a seller account!')
            return redirect('profile')
        else:
            messages.error(request, 'You are already a seller!')
    
    return render(request, 'accounts/switch_to_seller.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')
