from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SellerProfile

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=17, required=False, help_text='Enter your phone number.')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone_number']

class SellerRegistrationForm(UserCreationForm):
    business_name = forms.CharField(max_length=255, required=True, help_text='Enter your business name.')
    business_description = forms.CharField(widget=forms.Textarea, required=True, help_text='Enter a brief description of your business.')
    address = forms.CharField(max_length=255, required=True, help_text='Enter your business address.')
    city = forms.CharField(max_length=100, required=True, help_text='Enter your city.')
    state = forms.CharField(max_length=100, required=True, help_text='Enter your state.')
    postal_code = forms.CharField(max_length=20, required=True, help_text='Enter your postal code.')
    country = forms.CharField(max_length=100, required=True, help_text='Enter your country.')
    phone_number = forms.CharField(max_length=17, required=False, help_text='Enter your phone number.')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'business_name', 'business_description', 'address', 'city', 'state', 'postal_code', 'country', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit)
        SellerProfile.objects.create(
            user=user,
            business_name=self.cleaned_data['business_name'],
            business_description=self.cleaned_data['business_description'],
            address=self.cleaned_data['address'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            postal_code=self.cleaned_data['postal_code'],
            country=self.cleaned_data['country'],
        )
        return user

class SellerProfileEditForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = [
            'business_name',
            'business_description',
            'address',
            'city',
            'state',
            'postal_code',
            'country'
        ]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'default_shipping_address']