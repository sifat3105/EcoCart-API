from django.db import models
from orders.models import Order

class SalesReport(models.Model):
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    total_orders = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"Sales Report for {self.date}"

class UserActivity(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"
