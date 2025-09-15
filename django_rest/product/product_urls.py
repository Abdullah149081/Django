from django.urls import path
from product import views

urlpatterns = [
    path("", views.product_list_create, name="product-list-create"),
    path("<int:id>/", views.find_products_by_id, name="product-detail"),
]
