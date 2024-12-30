from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone_number = PhoneNumberField( region="BD", help_text="Enter a valid phone number.")
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

