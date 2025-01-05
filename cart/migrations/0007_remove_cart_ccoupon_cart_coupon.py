# Generated by Django 5.1.4 on 2025-01-05 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_cart_discount_applied_and_more'),
        ('discounts', '0006_alter_coupon_maximum_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='ccoupon',
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='discounts.coupon'),
        ),
    ]