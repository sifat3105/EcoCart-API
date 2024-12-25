from django.db import models
from products.models import Product

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock_level = models.PositiveIntegerField()

    def __str__(self):
        return f"Inventory for {self.product.name}"
