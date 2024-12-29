from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price_after_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total_price(self):
        return sum(item.quantity * item.product.price for item in self.items.all())
    
    # def save(self):
    #     if self.discount_applied == 0 and self.total_price_after_discount == 0:
    #         self.total_price_after_discount = self.get_total_price()
    #     elif self.discount_applied!=0:
    #         pass
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def get_total_price(self):
        return self.product.price * self.quantity
 