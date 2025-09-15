from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from product.models import Product, Category
from django.db.models import Count

from product.serializers import (
    CategorySerializer,
    CategoryCreateSerializer,
    ProductSerializer,
)


@api_view(["GET", "POST"])
def product_list_create(request):
    if request.method == "GET":
        products = Product.objects.select_related("category").all()
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data})

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def view_categories(request):
    if request.method == "GET":
        categories = Category.objects.annotate(product_count=Count("products")).all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data})

    elif request.method == "POST":
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(
                CategorySerializer(category).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def find_products_by_id(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response({"product": serializer.data})


@api_view(["GET"])
def find_category_by_id(request, id):
    category = get_object_or_404(Category, pk=id)
    serializer = CategorySerializer(category)
    return Response({"category": serializer.data})
