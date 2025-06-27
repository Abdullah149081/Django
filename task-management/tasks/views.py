from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForms
from tasks.models import Employee, Task
from django.contrib import messages


# Create your views here.


def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


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
