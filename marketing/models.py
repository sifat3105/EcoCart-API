from django.db import models

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class PromoBanner(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    active = models.BooleanField(default=True)
    display_start = models.DateTimeField()
    display_end = models.DateTimeField()

    def __str__(self):
        return self.title
