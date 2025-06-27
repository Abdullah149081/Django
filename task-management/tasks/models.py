from django.db import models

# Create your models here.


class Task(models.Model):
    PADDING = "PADDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    STATUS_CHOICES = (
        (PADDING, "Padding"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PADDING)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        default=1,  # Default to project with ID 1
    )
    assigned_to = models.ManyToManyField("Employee")

    def __str__(self):
        return self.title


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
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return (
            f"Details for {self.task.title} - Priority: {self.get_priority_display()}"
        )


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
