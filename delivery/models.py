from django.db import models
from django.contrib.auth.models import User



class DeliveryOption(models.Model):
    DELIVERY_TYPES = [
        ('standard', 'Standard Delivery'),
        ('express', 'Express Delivery'),
        ('pickup', 'Store Pickup'),
    ]
    name = models.CharField(max_length=50, choices=DELIVERY_TYPES ,default="standard")
    description = models.TextField(blank=True, null=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estimated_time = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_name_display()}"


class DeliveryAddress(models.Model):
    ZONE_TYPES = [
        ('1', 'Inside Dhaka'),
        ('2', 'Outside Dhaka'),
        ('3', 'Rajshahi'),
        ('4', 'Sylhet'),
        ('5', 'Chattogram'),
        ('6', 'Khulna'),
        ('7', 'Rangpur '),
        ('8', 'Barishal '),
        ('9', 'Mymensingh  '),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Bangladesh")
    zone = models.CharField(max_length=50, choices=ZONE_TYPES, unique=True)
    delivery_option = models.ForeignKey(DeliveryOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name}, {self.address_line_1}, {self.city}"


class Delivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_option = models.ForeignKey(DeliveryOption, on_delete=models.SET_NULL, null=True)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_delivery_charge(self):
        if self.delivery_option and self.delivery_address and self.delivery_address.zone:
            return self.delivery_option.get_delivery_charge(self.delivery_address.zone.name)
        return 0

    def __str__(self):
        return f"Delivery for {self.user.username} - {self.get_status_display()}"
