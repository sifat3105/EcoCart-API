from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart-detail'),
    path('item/<slug:product_slug>/', views.CartItemCreateView.as_view(), name='cart-item-add'),
    path('item/delete/<int:item_id>/', views.CartItemDeleteView.as_view(), name="cart-item-delete"),
    path('item/<int:cart_item_id>/<str:action>/', views.CartQuantityUpdateView.as_view(), name='quantity-update'),
]
