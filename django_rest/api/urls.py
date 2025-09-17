from django.urls import path, include
from rest_framework import routers  # For DefaultRouter
from rest_framework_nested import routers as nested_routers  # For NestedDefaultRouter

from product.views import CategoryViewSet, ProductViewSet, ReviewViewSet

# Main router for categories
router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet)

# Products router (parent)
products_router = routers.DefaultRouter()
products_router.register(r"products", ProductViewSet)

# Nested router for reviews under products
products_nested_router = nested_routers.NestedDefaultRouter(
    products_router,  # Parent router
    r"products",  # Parent URL prefix
    lookup="product",  # URL parameter name
)
products_nested_router.register(r"reviews", ReviewViewSet, basename="product-reviews")

urlpatterns = [
    path("", include(router.urls)),  # /categories/
    path("", include(products_router.urls)),  # /products/
    path("", include(products_nested_router.urls)),  # /products/{id}/reviews/
]
