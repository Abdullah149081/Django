# playground.py

import os
import django
from tabulate import tabulate
from django.core.exceptions import ValidationError

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_management.settings")
django.setup()

from tasks.models import Task, TaskDetail, Project


def print_table(data, headers, title="", tablefmt="fancy_grid"):
    """Utility function to print a table using tabulate."""
    if title:
        print(f"\n{title}")
    print(tabulate(data, headers=headers, tablefmt=tablefmt))


def main():
    task1 = Task.objects.create(
        title="Task 1",
        description="Description for Task 1",
        due_date="2023-12-31",
        is_completed=False,
    )
    task2 = Task.objects.create(
        title="Task 2",
        description="Description for Task 2",
        due_date="2024-01-15",
        is_completed=True,
    )

    task3 = Task.objects.create(
        title="Task 3",
        description="Description for Task 3",
        due_date="2024-02-28",
        is_completed=True,
    )


if __name__ == "__main__":
    main()
    print("Running playground.py...")
