from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart-detail'),
    path('item/<int:product_id>/', views.CartItemCreateView.as_view(), name='cart-item-add'),
    path('item/delete/<int:item_id>/', views.CartItemDeleteView.as_view(), name="cart-item-delete"),
]
