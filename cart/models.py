from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from discounts.models import Coupon

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_shipping_fee(self):
        shipping_fee = 70 if self.items.exists() else 0
        return self.shipping_fee


    def get_total_price(self):
        item_total = sum(item.quantity * item.product.price for item in self.items.all())
        return item_total 

    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def get_total_price(self):
        return self.product.price * self.quantity
 