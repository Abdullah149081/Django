from django.urls import path
from tasks.views import manager_dashboard


urlpatterns = [
    path("manager_dashboard/", manager_dashboard, name="manager_dashboard"),
]
