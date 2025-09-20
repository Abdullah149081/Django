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


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):  # type: ignore[override]
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

    def get_queryset(self):  # type: ignore[override]
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])
