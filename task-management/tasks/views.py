from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForms, TaskDetailForm
from tasks.models import Employee, Task
from django.contrib import messages
from django.db.models import Count, Q
from django.db import transaction


# Create your views here.

"""
Django ORM Query Optimization Tips:
| Situation                  | Use                              |
|----------------------------|----------------------------------|
| ForeignKey/OTM (OneToOne)  | select_related("field_name")     |
| ManyToMany or reverse FK   | prefetch_related("field_name")   |
| Need both                  | Combine them as needed           |
"""


def manager_dashboard(request):
    type = request.GET.get("type", "all")

    status_filter = {
        "pd": Task.PENDING,
        "in_progress": Task.IN_PROGRESS,
        "completed": Task.COMPLETED,
    }.get(type)

    tasks_qs = Task.objects.select_related("detail").prefetch_related("assigned_to")

    if status_filter:
        tasks = tasks_qs.filter(status=status_filter)
    else:
        tasks = tasks_qs.all()

    status_counts = Task.objects.aggregate(
        pd_tasks=Count("id", filter=Q(status=Task.PENDING)),
        in_progress_tasks=Count("id", filter=Q(status=Task.IN_PROGRESS)),
        completed_tasks=Count("id", filter=Q(status=Task.COMPLETED)),
    )

    context = {
        "tasks": tasks,
        "total_tasks": Task.objects.count(),
        "pd_tasks": status_counts["pd_tasks"],
        "in_progress_tasks": status_counts["in_progress_tasks"],
        "completed_tasks": status_counts["completed_tasks"],
    }
    return render(request, "dashboard/manager-dashboard.html", context)


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    """
    View to create a new task.
    Handles both Task and TaskDetail forms in a single transaction.
    On success, redirects and shows a success message.

    transaction.atomic() is used to ensure that both forms are saved together,
    and if any error occurs, the transaction is rolled back to maintain data integrity.
    """
    if request.method == "POST":
        form = TaskForms(request.POST)
        task_detail_form = TaskDetailForm(request.POST)
        if form.is_valid() and task_detail_form.is_valid():
            try:
                with transaction.atomic():
                    task = form.save()
                    task_detail = task_detail_form.save(commit=False)
                    task_detail.task = task
                    task_detail.save()
                messages.success(request, "Task created successfully!")
                return redirect("create_task")
            except Exception as e:
                messages.error(request, f"Error creating task: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForms()
        task_detail_form = TaskDetailForm()

    return render(
        request,
        "form.html",
        {
            "form": form,
            "task_detail_form": task_detail_form,
        },
    )


def view_tasks(request):
    """View to display all tasks.
    This view retrieves all tasks from the database and renders them in a template.
    """
    tasks = Task.objects.filter(status=Task.IN_PROGRESS)
    return render(request, "show.html", {"tasks": tasks})
