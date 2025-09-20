from django.db import models

# Create your models here.

# API Development Steps (as requested):
# Model - Define data structure
# Serializer - Convert models to/from JSON
# ViewSet - Handle HTTP requests
# Router - Configure URL routing


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    stock = models.PositiveIntegerField(db_index=True)
    image = models.ImageField(upload_to="products/images/", blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name", "category"]),
            models.Index(fields=["price", "stock"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["category", "price"]),
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["product", "-date"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"Review by {self.name} for {self.product.name}"
