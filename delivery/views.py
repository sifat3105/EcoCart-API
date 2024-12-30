from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializer import DeliveryZoneSerializer, DeliverySerializer, DeliveryAddressSerializer, DeliveryOptionSerializer
from . models import DeliveryZone, DeliveryOption, DeliveryAddress, Delivery


class DeliveryOptionview(APIView):
    def get(self):
        queryset = DeliveryOption.objects.all()
        serializer = DeliveryOptionSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeliveryZoneView(APIView):
    def get(self, request):
        deliveryzone = DeliveryZone.objects.all()
        serializer = DeliveryZoneSerializer(deliveryzone)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeliveryAddressListCreateView(ListCreateAPIView):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeliveryAddressDetailView(RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)
    
