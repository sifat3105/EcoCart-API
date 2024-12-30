from django.urls import path
from . import views

urlpatterns = [
    path('addresses/', views.DeliveryAddressListCreateView.as_view(), name='delivery-address-list-create'),
    path('addresses/<int:pk>/', views.DeliveryAddressDetailView.as_view(), name='delivery-address-detail'),
]
