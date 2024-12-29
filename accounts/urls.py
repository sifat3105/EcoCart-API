from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login_user'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/<str:username>/', views.UpdateUserProfileView.as_view(), name='update-user-profile'),
    
]
