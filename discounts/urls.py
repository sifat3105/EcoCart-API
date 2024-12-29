from django.urls import path
from .import views  
urlpatterns = [
    path('coupons/', views.CouponListCreateView.as_view(), name='coupon-list-create'),
    path('coupons/<int:pk>/', views.CouponDetailView.as_view(), name='coupon-detail'),
    path('coupons/apply/', views.CouponApplyView.as_view(), name='coupon-apply'),
]