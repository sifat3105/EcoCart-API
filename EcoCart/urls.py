from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('product/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('discounts/', include('discounts.urls')),
    path('delivery/', include('delivery.urls')),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
