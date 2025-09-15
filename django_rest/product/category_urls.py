from django.urls import path
from product import views

urlpatterns = [
    path("", views.view_categories, name="category-list"),
    path("<int:id>/", views.find_category_by_id, name="category-detail"),
]
