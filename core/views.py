from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer
from django.db.models import Count
import random


class CategoryList(generics.ListAPIView):
    # this view will return all categories
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class HomeCategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        queryset = queryset.annotate(random_order=Count("id"))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:5]


class BrandList(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        queryset = queryset.annotate(random_order=Count("id"))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]


class PopularProductsList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(ratings__gte=4.0, ratings__lte=5.0).all()
        queryset = queryset.annotate(random_order=Count("id"))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]


class ProductListByClothesType(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        query = request.query_params.get("clothes_type", None)
        if query:
            queryset = Product.objects.filter(clothes_type=query)
            queryset = queryset.annotate(random_order=Count("id"))
            product_list = list(queryset)
            random.shuffle(product_list)
            limited_products = product_list[:20]
            serializer = ProductSerializer(limited_products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Please provide a clothes_type query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SimilarProducts(APIView):
    def get(self, request):
        query = request.query_params.get("category", None)

        if query:
            products = Product.objects.filter(category=query)
            product_list = list(products)
            random.shuffle(product_list)
            limited_products = product_list[:6]
            serialzier = ProductSerializer(limited_products, many=True)
            return Response(serialzier.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Please provide a category query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SearchProductByTitle(APIView):
    def get(self, request):
        query = request.query_params.get("q", None)

        if query:
            products = Product.objects.filter(title__icontains=query)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Please provide a query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FilterProductsByCategory(APIView):
    def get(self, request):
        query = request.query_params.get("category", None)

        if query:
            products = Product.objects.filter(category=query)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Please provide a category query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
