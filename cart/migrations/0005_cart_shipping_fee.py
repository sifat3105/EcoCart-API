# Generated by Django 5.1.4 on 2025-01-03 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cart_discount_applied_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='shipping_fee',
            field=models.DecimalField(decimal_places=2, default=70, max_digits=10),
        ),
    ]