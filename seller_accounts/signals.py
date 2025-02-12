from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, SalesAnalytics

@receiver(post_save, sender=Order)
def update_seller_analytics(sender, instance, **kwargs):
    if instance.seller.analytics:
        instance.seller.analytics.update_sales()
    else:
        SalesAnalytics.objects.create(seller=instance.seller)
