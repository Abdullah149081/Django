from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForms
from tasks.models import Employee, Task
from django.contrib import messages


# Create your views here.


def manager_dashboard(request):
    try:
        tasks = Task.objects.all()
        context = {
            "tasks": tasks,
            "total_tasks": tasks.count(),
            "pd_tasks": tasks.filter(status=Task.PENDING).count(),
            "in_progress_tasks": tasks.filter(status=Task.IN_PROGRESS).count(),
            "completed_tasks": tasks.filter(status=Task.COMPLETED).count(),
        }
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {e}")
        context = {
            "tasks": [],
            "total_tasks": 0,
            "pd_tasks": 0,
            "in_progress_tasks": 0,
            "completed_tasks": 0,
        }
    return render(request, "dashboard/manager-dashboard.html", context)


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    """View to create a new task.
    This view handles the creation of a new task by processing the form submission.
    If the form is valid, it saves the task and redirects to the same page with a success message.
    """
    form = TaskForms()

    if request.method == "POST":
        form = TaskForms(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully!")  # ✅ here
            return redirect("create_task")
    return render(
        request,
        "form.html",
        {"form": form, "success": "Task created successfully!"},
    )


def view_tasks(request):
    """View to display all tasks.
    This view retrieves all tasks from the database and renders them in a template.
    """
    tasks = Task.objects.filter(status=Task.IN_PROGRESS)
    return render(request, "show.html", {"tasks": tasks})
