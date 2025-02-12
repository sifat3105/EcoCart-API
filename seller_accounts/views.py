from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from .forms import SellerSignupForm, SellerLoginForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Seller
import random

User = get_user_model()


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(request, email, otp):
    current_site = get_current_site(request)
    domain = current_site.domain
    subject = "Verify Your Email Address"
    subject = "Verify Your Email Address"
    message = f"Your OTP for email verification is: {otp}\n\n"
    message += f"If you did not request this, please ignore this email.\n\n"
    message += f"Thank you,\n{domain} Team"
    send_mail(subject, message, f"noreply@example.com", [email], fail_silently=False,)


def seller_register(request):
    if request.method == "POST":
        form = SellerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            otp = generate_otp()
            seller = form.instance
            seller.otp = otp
            seller.save()
            send_otp_email(request, user.email, otp)
            return redirect("accounts:verify_otp", user_id=user.id)
    else:
        form = SellerSignupForm()
    return render(request, "accounts/register.html", {"form": form})


def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)
    seller = get_object_or_404(Seller, user=user)

    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        if seller.otp == otp_entered:
            seller.is_active = True
            seller.otp = None
            seller.save()
            user.is_active = True
            user.save()
            return redirect("accounts:login", {"message": "Your account has been successfully verified and activated."} )
        else:
            return render(request, "accounts/verify_otp.html", {"error": "Invalid OTP"})

    return render(request, "accounts/verify_otp.html")


def seller_login(request):
    if request.method == "POST":
        form = SellerLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("accounts:seller_dashboard")
            else:
                return render(request, "accounts/seller_login.html", {"form": form, "error": "Invalid username or password."})
    else:
        form = SellerLoginForm()
    return render(request, "accounts/seller_login.html", {"form": form})


def seller_logout(request):
    logout(request)
    return redirect("login")



