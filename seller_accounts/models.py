from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    business_license = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    

class SalesAnalytics(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE, related_name="analytics")
    total_sales = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_refunds = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def update_sales(self):
        completed_orders = self.seller.orders.filter(status="Completed")
        self.total_sales = completed_orders.count()
        self.total_revenue = sum(order.total_price for order in completed_orders)
        self.total_refunds = sum(order.total_price for order in self.seller.orders.filter(status="Canceled"))
        self.save()

    def __str__(self):
        return f"Analytics for {self.seller.store_name}"