from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, create_task


urlpatterns = [
    path("manager_dashboard/", manager_dashboard, name="manager_dashboard"),
    path("user_dashboard/", user_dashboard, name="user_dashboard"),
    path("create_task/", create_task, name="create_task"),
]
