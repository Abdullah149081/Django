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
                user = form.save(commit=False)
                user.set_password(form.cleaned_data.get("password1"))
                user.is_active = False  # Set user as inactive until email confirmation
                user.save()  # This will trigger the post_save signal to send email

                messages.success(
                    request,
                    f"Account created for {user.username}! Please check your email to activate your account.",
                )
                return redirect("sign_in")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "auth/signUp.html", {"form": form})


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if user exists
        try:
            user_obj = User.objects.get(username=username)
            if not user_obj.is_active:
                messages.error(
                    request,
                    "Your account is not activated. Please check your email for activation link.",
                )
                return render(request, "auth/login.html")
        except User.DoesNotExist:
            pass  # Will be handled by authenticate below

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Welcome back!")
                return redirect("manager_dashboard")
            else:
                messages.error(
                    request,
                    "Your account is not activated. Please check your email for activation link.",
                )
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html")


def sign_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("sign_in")
