from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required as login_required_all
from django.contrib import messages
from .forms import BuyerRegistrationForm, SellerRegistrationForm, BuyerProfileEditForm, SellerProfileEditForm
from .models import BuyerUser, SellerUser, BUYER, SELLER
from .decorators import login_required_custom_user  

login_required = login_required_custom_user()

def register_buyer(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Buyer account created successfully!")
            return redirect('login')  # Redirect to login or another page
    else:
        form = BuyerRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.user.is_buyer:
        return render(request, 'accounts/buyer_profile.html')    
    elif request.user.is_seller:
        return render(request, 'accounts/seller_profile.html')
    else:
        return redirect('home')

@login_required
def switch_to_seller(request):
    if request.method == 'POST':
        form = SellerProfileEditForm(request.POST)
        if form.is_valid():

            print(form.cleaned_data)
            kwargs = {
                'business_name': form.cleaned_data['business_name'],
                'business_description': form.cleaned_data['business_description'],
                'address': form.cleaned_data['address'],
                'city': form.cleaned_data['city'],
                'state': form.cleaned_data['state'],
                'postal_code': form.cleaned_data['postal_code'],
                'country': form.cleaned_data['country'],
            }
            # Switch user account type to seller
            request.user.switch_to_seller(**kwargs)
            messages.success(request, 'You have successfully switched to a seller account!')
            return redirect('profile')
    else:
        form = SellerProfileEditForm()

    return render(request, 'accounts/switch_to_seller.html', {'form': form})

def login_user(request):
    username_error = None
    password_error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            # Check if the user exists
            if BuyerRegistrationForm().Meta.model.objects.filter(username=username).exists():
                password_error = "Incorrect password. Please try again."
            else:
                username_error = "User does not exist. Please check your username."
        else:
            login(request, user)
            return redirect('home')
    
    return render(request, 'accounts/login.html', {
        'username_error': username_error,
        'password_error': password_error,
    })

@login_required_all
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Seller account created successfully!")
            return redirect('login')  # Redirect to login or another page
    else:
        form = SellerRegistrationForm()
    
    return render(request, 'accounts/register_seller.html', {'form': form})

@login_required
def edit_profile(request):
    user = request.user
    if user.is_seller:
        seller_profile = user.seller_profile
        if request.method == 'POST':
            profile_form = BuyerProfileEditForm(request.POST, instance=user)  # Handle user fields
            seller_form = SellerProfileEditForm(request.POST, instance=seller_profile)  # Handle seller fields
            if profile_form.is_valid() and seller_form.is_valid():
                profile_form.save()  # Save user fields
                seller_form.save()  # Save seller fields
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')  # Redirect to the seller profile view
        else:
            profile_form = BuyerProfileEditForm(instance=user)  # Pre-fill user fields
            seller_form = SellerProfileEditForm(instance=seller_profile)  # Pre-fill seller fields
    else:
        if request.method == 'POST':
            form = BuyerProfileEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')  # Redirect to the profile view
        else:
            profile_form = BuyerProfileEditForm(instance=user)

    return render(request, 'accounts/edit_profile.html', {
        'profile_form': profile_form,
        'seller_form': seller_form if user.is_seller else None
    })
