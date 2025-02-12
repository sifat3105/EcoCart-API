from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Seller

class SellerSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Seller
        fields = ['shop_name', 'business_license', 'address', 'phone']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        seller = super().save(commit=False)
        seller.user = user
        if commit:
            seller.save()
        return user

class SellerLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        try:
            seller = Seller.objects.get(user=user)
            if not seller.is_verified:
                raise ValidationError("Your account is not verified. Please complete the OTP verification process.")
        except Seller.DoesNotExist:
            raise ValidationError("You are not registered as a seller.")