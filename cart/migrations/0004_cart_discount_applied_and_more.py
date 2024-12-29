# Generated by Django 5.1.4 on 2024-12-29 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cart_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='discount_applied',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cart',
            name='total_price_after_discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
