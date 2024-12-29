from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CartSerializer, CartItemSerializer
from .models import Cart, CartItem
from products.models import Product

class CartView(APIView):
    def get(self, request):
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            serializer = CartSerializer(cart)  # pass the Cart instance, not the tuple
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

class CartItemCreateView(APIView):
    def post(self, request, product_id):
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
class CartItemDeleteView(APIView):
    def delete(self, request, item_id):
        try:
            cart = Cart.objects.get(user = request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)




