from rest_framework import serializers
from .models import CheckOut, CheckOutItem
from products.models import Product
from delivery.models import Delivery
from decimal import Decimal



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']

class CheckOutItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CheckOutItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price

class CheckOutSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = CheckOutItemSerializer(many=True)
    shipping_fee = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    

    class Meta:
        model = CheckOut
        fields = ['id', 'user', 'created_at', 'items', 'subtotal', 'shipping_fee', 'discount', 'total']

    def get_discount(self, obj):
        return (
            min(
                Decimal(obj.get_total_price()) * Decimal(obj.coupon.discount_percentage) / 100,
                obj.coupon.maximum_discount,
            )
            if hasattr(obj, 'coupon') and obj.coupon
            else Decimal(0)
        )
        

    def get_subtotal(self, obj):
        total_items = sum(item.quantity for item in obj.items.all())
        total_price = Decimal(obj.get_total_price())
        return {f"Subtotal ({total_items} items)": float(total_price)}

    def get_total(self, obj):
        discount = self.get_discount(obj)
        total_price = Decimal(obj.get_total_price())
        return total_price - discount + Decimal(self.get_shipping_fee(obj))
    
    def get_shipping_fee(self, obj):
        user = self.context.get('user')
        try:
            delivery = Delivery.objects.select_related('delivery_option').get(user=user)
            delivery_fee = delivery.delivery_option.delivery_fee
        except Delivery.DoesNotExist:
            delivery_fee = 70
        return delivery_fee if obj.items.exists() else 0