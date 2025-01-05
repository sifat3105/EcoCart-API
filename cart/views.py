from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializer import CartSerializer, CartItemSerializer
from .models import Cart, CartItem
from products.models import Product

class CartView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            serializer = CartSerializer(cart, context={'user': request.user})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

class CartItemCreateView(APIView):
    def post(self, request, product_slug):
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            try:
                product = Product.objects.get(slug=product_slug)
            except Product.DoesNotExist:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item.quantity += 1
                cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
class CartItemDeleteView(APIView):
    def delete(self, request, item_id):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()

            total_price = cart.get_total_price()
            try:
                coupon = cart.coupon
                if total_price < coupon.minimum_spend:
                    cart.coupon = None
                    cart.save()
            except AttributeError:
                pass

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

class CartQuantityUpdateView(APIView):
    def post(self, request, cart_item_id, action):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        
        if action == 'up':
            cart_item.quantity += 1
            cart_item.save()
            return Response({"message": "Quantity increased successfully", "quantity": cart_item.quantity}, status=status.HTTP_200_OK)
        
        elif action == 'down':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                return Response({"message": "Quantity decreased successfully", "quantity": cart_item.quantity}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Quantity cannot be less than 1"}, status=status.HTTP_400_BAD_REQUEST)

        
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)



