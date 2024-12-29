from django.urls import path
from .views import ProductListView, ProductCreateView, ProductView, CategoryCreateView, ProductSearchView

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<slug:product_slug>/', ProductView.as_view(), name='product-detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('', ProductSearchView.as_view(), name='product-search'),
]