from django.urls import path
from . import views

urlpatterns = [
    path('option/', views.DeliveryOptionview.as_view(), name='delivery-option-list'),
    path('option/<str:deliveryoption_name>', views.DeliveryOptionview.as_view(), name='delivery-option-choise'),
    path('addresses/', views.DeliveryAddressListCreateView.as_view(), name='delivery-address-list-create'),
    path('addresses/<int:pk>/', views.DeliveryAddressDetailView.as_view(), name='delivery-address-detail'),
]
