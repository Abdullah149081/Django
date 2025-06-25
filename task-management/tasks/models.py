from django.db import models

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        default=1,  # Default to project with ID 1
    )
    assigned_to = models.ManyToManyField("Employee")


class TaskDetail(models.Model):
    high = "H"
    medium = "M"
    low = "L"

    PRIORITY_CHOICES = (
        (low, "Low"),
        (medium, "Medium"),
        (high, "High"),
    )

    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=medium)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="detail")


class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
