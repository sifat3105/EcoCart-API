from rest_framework import serializers
from .models import DeliveryZone, DeliveryOption, DeliveryAddress, Delivery

class DeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZone
        fields = ['id', 'name', 'delivery_charge']


class DeliveryOptionSerializer(serializers.ModelSerializer):
    zone = DeliveryZoneSerializer(many=True, read_only=True)

    class Meta:
        model = DeliveryOption
        fields = ['id', 'name', 'delivery_fee', 'estimated_time', 'zone']


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = [
            'id', 'user', 'full_name', 'phone_number', 'address_line_1',
            'address_line_2', 'city', 'state', 'postal_code', 'country', 'zone'
        ]
        extra_kwargs = {
            'user': {'read_only': True}
        }


class DeliverySerializer(serializers.ModelSerializer):
    delivery_option = DeliveryOptionSerializer(read_only=True)
    delivery_address = DeliveryAddressSerializer(read_only=True)
    total_delivery_charge = serializers.SerializerMethodField()

    class Meta:
        model = Delivery
        fields = [
            'id', 'user', 'delivery_option', 'delivery_address', 'status',
            'tracking_number', 'created_at', 'updated_at', 'total_delivery_charge'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_delivery_charge(self, obj):
        return obj.calculate_total_delivery_charge()
