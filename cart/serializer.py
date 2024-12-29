from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price

class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total_price', 'discount_applied', 'total_price_after_discount']

    def get_total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.items.all())

