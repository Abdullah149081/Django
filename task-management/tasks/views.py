from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForms, TaskDetailForm
from tasks.models import Employee, Task, TaskDetail
from django.contrib import messages
from django.db.models import Count, Q
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods


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


@require_http_methods(["GET", "POST"])
def delete_task(request, task_id):
    """
    View to delete a task with confirmation and error handling.
    """
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        try:
            task.delete()
            messages.success(request, "Task deleted successfully!")
            return redirect("manager_dashboard")
        except Exception as e:
            messages.error(request, f"Error deleting task: {e}")
            return redirect("manager_dashboard")
    return render(request, "manager_dashboard.html", {"task": task})


def view_tasks(request):
    """View to display all tasks.
    This view retrieves all tasks from the database and renders them in a template.
    """
    tasks = Task.objects.filter(status=Task.IN_PROGRESS)
    return render(request, "show.html", {"tasks": tasks})


def handle_task_forms(request, task=None):
    """
    Handles both create and update logic for Task and TaskDetail.
    Returns (task_form, task_detail_form, success, redirect_url, is_create).
    """
    is_create = task is None
    task_form = TaskForms(request.POST or None, instance=task)
    task_detail_instance = getattr(task, "detail", None) if task else None
    task_detail_form = TaskDetailForm(
        request.POST or None, instance=task_detail_instance
    )

    if request.method == "POST":
        if task_form.is_valid() and task_detail_form.is_valid():
            try:
                with transaction.atomic():
                    task = task_form.save(commit=False)
                    task.save()
                    task_form.save_m2m()

                    task_detail = task_detail_form.save(commit=False)
                    task_detail.task = task
                    task_detail.save()

                messages.success(
                    request,
                    f"Task {'created' if is_create else 'updated'} successfully!",
                )
                return task_form, task_detail_form, True, "manager_dashboard", is_create
            except Exception as e:
                messages.error(
                    request,
                    f"An error occurred while {'creating' if is_create else 'updating'} task: {e}",
                )
        else:
            messages.error(request, "Please correct the errors below.")

    return task_form, task_detail_form, False, None, is_create


def create_task(request):
    task_form, task_detail_form, success, redirect_url, is_create = handle_task_forms(
        request
    )
    if success:
        return redirect(redirect_url)
    return render(
        request,
        "form.html",
        {
            "task_form": task_form,
            "task_detail_form": task_detail_form,
            "is_create": is_create,
        },
    )


def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task_form, task_detail_form, success, redirect_url, is_create = handle_task_forms(
        request, task
    )
    if success:
        return redirect(redirect_url)
    return render(
        request,
        "form.html",
        {
            "task_form": task_form,
            "task_detail_form": task_detail_form,
            "is_create": is_create,
        },
    )


# def create_task(request):
#     if request.method == "POST":
#         task_form = TaskForms(request.POST)
#         task_detail_form = TaskDetailForm(request.POST)
#         if task_form.is_valid() and task_detail_form.is_valid():
#             task = task_form.save(commit=False)  # <-- commit=False here
#             task_detail = task_detail_form.save(commit=False)
#             task.save()  # <-- save model instance first
#             task_form.save_m2m()  # <-- now save many-to-many
#             task_detail.task = task
#             task_detail.save()
#             messages.success(request, "Task created successfully!")
#             return redirect("manager_dashboard")
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         task_form = TaskForms()
#         task_detail_form = TaskDetailForm()

#     return render(
#         request,
#         "form.html",
#         {
#             "task_form": task_form,
#             "task_detail_form": task_detail_form,
#             "is_create": True,
#         },
#     )


# def update_task(request, task_id):
#     task = Task.objects.get(id=task_id)
#     try:
#         task_detail = task.detail
#     except TaskDetail.DoesNotExist:
#         task_detail = None

#     if request.method == "POST":
#         task_form = TaskForms(request.POST, instance=task)
#         task_detail_form = TaskDetailForm(request.POST, instance=task_detail)
#         if task_form.is_valid() and task_detail_form.is_valid():
#             task = task_form.save(commit=False)
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task.save()
#             # Save the many-to-many data properly:
#             task_form.save_m2m()
#             task_detail.save()

#             messages.success(request, "Task Updated Successfully")
#             return redirect("manager_dashboard")
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         task_form = TaskForms(instance=task)
#         task_detail_form = TaskDetailForm(instance=task_detail)

#     context = {"task_form": task_form, "task_detail_form": task_detail_form}
#     return render(request, "form.html", context)
