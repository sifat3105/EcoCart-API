from django.db import models

class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class ShippingRate(models.Model):
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Shipping to {self.country} via {self.shipping_method.name}"
