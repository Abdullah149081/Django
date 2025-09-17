from django.urls import path
from product import views

urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view({"get": "list", "post": "create"}),
        name="category-list",
    ),
    path(
        "<int:id>/",
        views.CategoryViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="category-detail",
    ),
]
