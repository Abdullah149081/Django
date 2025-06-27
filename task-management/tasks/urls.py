from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, create_task, view_tasks
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("manager_dashboard/", manager_dashboard, name="manager_dashboard"),
    path("user_dashboard/", user_dashboard, name="user_dashboard"),
    path("create_task/", create_task, name="create_task"),
    path(
        "view_tasks/", view_tasks, name="view_tasks"
    ),  # Assuming view_tasks is the correct view for this URL
] + debug_toolbar_urls()  # Include Debug Toolbar URLs if installed
