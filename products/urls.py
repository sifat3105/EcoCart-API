from django.urls import path
from .views import ProductListView, ProductCreateView

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
]