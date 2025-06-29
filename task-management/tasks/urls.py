from django.urls import path
from tasks.views import (
    manager_dashboard,
    user_dashboard,
    create_task,
    view_tasks,
    update_task,
    delete_task,
)
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("manager_dashboard/", manager_dashboard, name="manager_dashboard"),
    path("user_dashboard/", user_dashboard, name="user_dashboard"),
    path("create_task/", create_task, name="create_task"),
    path(
        "view_tasks/", view_tasks, name="view_tasks"
    ),  # Assuming view_tasks is the correct view for this URL
    path("update_task/<int:task_id>/", update_task, name="update_task"),
    path("delete_task/<int:task_id>/", delete_task, name="delete_task"),
] + debug_toolbar_urls()  # Include Debug Toolbar URLs if installed
