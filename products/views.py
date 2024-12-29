from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer,ProductDetailsSerializer, CategorySerializer
from .models import Product, Category



class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        products = products[start:end]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ProductCreateView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)
        return Response(categories_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductView(APIView):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        serializer = ProductDetailsSerializer(product)
        return Response(serializer.data)

    
class ProductSearchView(APIView):
    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)
        category = request.query_params.get('category', None)
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))

        if not search_query:
            return Response({"error": "Search query is required."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Product.objects.all()

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        if category:
            queryset = queryset.filter(category__name=category)

        start = (page - 1) * page_size
        end = start + page_size
        products = queryset[start:end]

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    