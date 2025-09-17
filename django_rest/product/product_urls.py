from django.urls import path
from product import views

urlpatterns = [
    path(
        "",
        views.ProductViewSet.as_view({"get": "list", "post": "create"}),
        name="product-list-create",
    ),
    path(
        "<int:id>/",
        views.ProductViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="product-detail",
    ),
]
