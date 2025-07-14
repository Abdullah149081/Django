from django.shortcuts import render, redirect
from django.contrib import messages
from users.form import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                form.save()
                username = form.cleaned_data.get("username")
                messages.success(request, f"Account created for {username}!")
                return redirect("sign_up")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "auth/signUp.html", {"form": form})


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("manager_dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "auth/login.html")


def sign_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("sign_in")
