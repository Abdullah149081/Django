from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category, Review
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from product.pagination import DefaultPagination

from product.serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ["name", "description"]
    ordering_fields = ["price", "name", "stock"]

    def get_queryset(self):  # type: ignore[override]
        """Optimize queries with select_related to avoid N+1 problems"""
        return Product.objects.select_related("category").prefetch_related("reviews")

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response(
                {"error": "Cannot delete a product with stock greater than ten."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.perform_destroy(product) or Response(
            status=status.HTTP_204_NO_CONTENT
        )


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):  # type: ignore[override]
        """Optimize category queries with product count annotation"""
        return Category.objects.annotate(
            product_count=Count("products")
        ).prefetch_related("products")


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    filter_backends = [OrderingFilter]
    pagination_class = DefaultPagination
    ordering_fields = ["name"]

    def get_queryset(self):  # type: ignore[override]
        """Optimize review queries with product relationship"""
        return Review.objects.select_related("product").filter(
            product_id=self.kwargs["product_pk"]
        )

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
