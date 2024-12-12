from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, SellerRegistrationForm, ProfileEditForm, SellerProfileEditForm
from .models import BuyerProfile, SellerProfile

def register_buyer(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.account_type = 'BUYER'  # Set account type to BUYER
            user.save()
            BuyerProfile.objects.create(user=user)  # Create buyer profile
            messages.success(request, "Buyer account created successfully!")
            return redirect('login')  # Redirect to login or another page
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
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            # Switch user account type to seller
            request.user.switch_to_seller()
            # Save additional seller information
            SellerProfile.objects.create(
                user=request.user,
                business_name=form.cleaned_data['business_name'],
                business_description=form.cleaned_data['business_description'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data['country'],
            )
            messages.success(request, 'You have successfully switched to a seller account!')
            return redirect('profile')
    else:
        form = SellerRegistrationForm()

    return render(request, 'accounts/switch_to_seller.html', {'form': form})

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

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Seller account created successfully!")
            return redirect('login')  # Redirect to login or another page
    else:
        form = SellerRegistrationForm()
    
    return render(request, 'accounts/register_seller.html', {'form': form})

@login_required
def edit_profile(request):
    user = request.user
    if user.account_type == 'SELLER':
        seller_profile = user.seller_profile
        if request.method == 'POST':
            form = SellerProfileEditForm(request.POST, instance=seller_profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Seller profile updated successfully!")
                return redirect('profile')  # Redirect to the seller profile view
        else:
            form = SellerProfileEditForm(instance=seller_profile)
    else:
        if request.method == 'POST':
            form = ProfileEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')  # Redirect to the profile view
        else:
            form = ProfileEditForm(instance=user)

    return render(request, 'accounts/edit_profile.html', {'form': form})
