from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CheckOutCreateView.as_view(), name='checkout-create'),
    path('direct/<slug:product_slug>/', views.DirectCheckOutView.as_view(), name='direct-checkout'),
    path('', views.Checkoutview.as_view(), name='checkout-view'),
    path('coupons/apply/', views.CheckOutCouponApplyView.as_view(), name='checkout-coupon-apply'),
    path('item/<int:checkout_item_id>/<str:action>/', views.QuantityUpdateView.as_view(), name='checkout-item-quantity-update'),
]
