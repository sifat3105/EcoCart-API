from rest_framework import serializers
from .models import Product, Category, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductDetailsSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )
    product_images = ProductImageSerializer(many=True, read_only=True, source='images')

    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'description', 'price', 'stock', 'image', 'images', 'product_images']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)

        for image_data in images_data:
            ProductImage.objects.create(product=product, image=image_data)

        return product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category','price', 'stock', 'image',]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


