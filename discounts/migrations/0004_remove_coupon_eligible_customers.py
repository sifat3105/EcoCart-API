# Generated by Django 5.1.4 on 2024-12-29 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0003_alter_coupon_valid_from_alter_coupon_valid_until'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='eligible_customers',
        ),
    ]
