from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Coupon
from .serializer import CouponSerializer
from django.utils import timezone
from decimal import Decimal

class CouponListCreateView(ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class CouponDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class CouponApplyView(APIView):
    def get(self, request):
        coupons = Coupon.objects.all()
        valid_coupons = filter(lambda coupon: coupon.is_applicable(request) and timezone.now().date() < coupon.valid_until, coupons)
        serializer = CouponSerializer(valid_coupons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        coupon_code = request.data.get('coupon_code')
        if not coupon_code:
            return Response({"detail": "Coupon code is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return Response({"detail": "Invalid coupon code."}, status=status.HTTP_400_BAD_REQUEST)
        cart = getattr(request.user, 'cart', None)
        if not cart:
            return Response({"detail": "User cart not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        cart.coupon = coupon
        cart.save()
        return Response({"detail": "Coupon applied successfully."}, status=status.HTTP_200_OK)

