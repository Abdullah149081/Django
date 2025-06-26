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
    # employees = Employee.objects.all()
    form = TaskForms()

    if request.method == "POST":
        form = TaskForms(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully!")  # ✅ here
            return redirect("create_task")

            # Django forms Data
            # print("Task created with data:", form.cleaned_data)
            # data = form.cleaned_data

            # task = Task.objects.create(
            #     title=data["title"],
            #     description=data["description"],
            #     due_date=data["due_date"],
            # )
            # assigned_to = data["assigned_to"]

            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task created successfully!")
    return render(
        request,
        "form.html",
        {"form": form, "success": "Task created successfully!"},
    )
