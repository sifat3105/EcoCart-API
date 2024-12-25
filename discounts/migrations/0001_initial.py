# Generated by Django 5.1.4 on 2024-12-25 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount_percentage', models.PositiveIntegerField()),
                ('valid_from', models.DateTimeField()),
                ('valid_until', models.DateTimeField()),
            ],
        ),
    ]
