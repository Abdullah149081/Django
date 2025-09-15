from rest_framework import serializers
from decimal import Decimal
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField(method_name="get_product_count")

    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]

    def get_product_count(self, obj):
        return getattr(obj, "product_count", 0)


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "tax",
        ]

    tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product) -> Decimal:
        return (product.price * Decimal("1.2")).quantize(Decimal("0.01"))

    def validate_stock(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate_price(self, value: float) -> float:
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
