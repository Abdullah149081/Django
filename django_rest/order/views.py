from django.shortcuts import render
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from order.serializers import (
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
)
from order.models import Cart, CartItem

# Create your views here.


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = CartSerializer

    def get_queryset(self):  # type: ignore[override]
        """Optimize cart queries with prefetch_related to avoid N+1 problems"""
        return Cart.objects.prefetch_related(
            "items__product__category"  # Prefetch cart items with their products and categories
        ).select_related("user")
