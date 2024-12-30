# Generated by Django 5.1.4 on 2024-12-30 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0005_coupon_maximum_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='maximum_discount',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10),
        ),
    ]
