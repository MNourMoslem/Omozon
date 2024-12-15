from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import DeliveryManagerUser
from accounts.models import CustomUser, DELIVERY_MANAGER

class DeliveryRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password1")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                raise forms.ValidationError("A user with that username already exists.")

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            account_type=DELIVERY_MANAGER
        )
        if commit:
            user.save()
        return DeliveryManagerUser.objects.create(user=user)

class DeliveryLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
        return cleaned_data