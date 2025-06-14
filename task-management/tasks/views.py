from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    """Render a simple view that returns a name.
    Args:
        request: The HTTP request object.
    """
    return HttpResponse("Hello, World!")


def contact(request):
    """Render a contact page.
    Args:
        request: The HTTP request object.
    """
    return HttpResponse("Contact us at contact@example.com")


def show_task(request):
    """Render a task page.
    Args:
        request: The HTTP request object.
    """
    return HttpResponse("This is a task page.")