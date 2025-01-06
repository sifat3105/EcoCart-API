from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CheckOutSerializer
from .models import CheckOut, CheckOutItem
from cart.models import Cart, CartItem
from products.models import Product
from discounts.models import Coupon
from django.shortcuts import get_object_or_404

class CheckOutCreateView(APIView):
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        check_out, created = CheckOut.objects.get_or_create(user=request.user,)
        if cart.coupon:
            check_out.coupon = cart.coupon
            check_out.save()
        
        for cart_item in cart_items:
            CheckOutItem.objects.get_or_create(
                checkout=check_out,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        
        cart_items.delete()
        
        return Response({"message": "Checkout created successfully"}, status=status.HTTP_200_OK)

class DirectCheckOutView(APIView):
    def post(self, request, product_slug):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            product = Product.objects.get(slug=product_slug)
            check_out = CheckOut.objects.get_or_create(user=request.user)
            check_out_item = CheckOutItem.objects.create(checkout=check_out,product=product)
            check_out_item.quantity += 1
            check_out_item.save()
            return Response({"message": "Checkout created successfully"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

            
class Checkoutview(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            check_out = CheckOut.objects.get(user=request.user)
            serializer = CheckOutSerializer(check_out)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"detail": "CheckOut not found."}, status=status.HTTP_404_NOT_FOUND)

class CheckOutCouponApplyView(APIView):
    def post(self, request):
        coupon_code = request.data.get('coupon_code')
        if not coupon_code:
            return Response({"detail": "Coupon code is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return Response({"detail": "Invalid coupon code."}, status=status.HTTP_400_BAD_REQUEST)
        checkout = getattr(request.user, 'checkout', None)
        if not checkout:
            return Response({"detail": "User CheckOut not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        checkout.coupon = coupon
        checkout.save()
        return Response({"detail": "Coupon applied successfully."}, status=status.HTTP_200_OK)
    

class QuantityUpdateView(APIView):
    def post(self, request, checkout_item_id, action):
        checkout_item = get_object_or_404(CheckOutItem, id=checkout_item_id, checkout__user=request.user)
        
        if action == 'up':
            checkout_item.quantity += 1
            checkout_item.save()
            return Response({"message": "Quantity increased successfully", "quantity": checkout_item.quantity}, status=status.HTTP_200_OK)
        
        elif action == 'down':
            if checkout_item.quantity > 1:
                checkout_item.quantity -= 1
                checkout_item.save()
                return Response({"message": "Quantity decreased successfully", "quantity": checkout_item.quantity}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Quantity cannot be less than 1"}, status=status.HTTP_400_BAD_REQUEST)
        
        elif action == 'delete':
            checkout_item.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)