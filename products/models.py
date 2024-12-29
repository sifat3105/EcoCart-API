from django.db import models
import uuid
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.CharField(max_length=50, unique=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + str(uuid.uuid4().hex[:6])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"
