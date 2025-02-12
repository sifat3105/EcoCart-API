from django.urls import path
from .views import seller_register, seller_login, seller_logout, verify_otp

urlpatterns = [
    path("register/", seller_register, name="register"),
    path("login/", seller_login, name="login"),
    path("logout/", seller_logout, name="logout"),
    path("verify-otp/<int:user_id>/", verify_otp, name="verify_otp")
]

