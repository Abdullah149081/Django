# playground.py

import os
import django
from tabulate import tabulate
from django.core.exceptions import ValidationError

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_management.settings")
django.setup()

from tasks.models import Task, TaskDetail, Project, Employee


def print_table(data, headers, title="", tablefmt="fancy_grid"):
    """Utility function to print a table using tabulate."""
    if title:
        print(f"\n{title}")
    print(tabulate(data, headers=headers, tablefmt=tablefmt))


def main():
    # Welcome message
    print("Welcome to the Task Management Playground!")

    TaskDetail.objects.create(
        task=Task.objects.get(id=2),
        assigned_to="Jane Smith",
        priority="M",  # Use a single character as per the model's field definition
    )

    # Display all tasks
    # print_table("")


if __name__ == "__main__":
    main()
    print("Running playground.py...")
