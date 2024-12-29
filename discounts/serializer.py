from rest_framework import serializers
from .models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_percentage','maximum_discount', 'minimum_spend', 'valid_from', 'valid_until']
