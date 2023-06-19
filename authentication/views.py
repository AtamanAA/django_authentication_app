from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import RegisterUserForm, LoginUserForm


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email):
                messages.error(
                    request,
                    (f"Email {email} is already in use! Choose another."),
                )
                return render(request, "authentication/register.html", {"form": form})
            else:
                form.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, ("You have successfully registered!"))
                return redirect("index")
    else:
        form = RegisterUserForm()

    return render(request, "authentication/register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, ("Username or password is incorrect, try again!"))
            return redirect("login")
    else:
        form = LoginUserForm()
        return render(request, "authentication/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, ("You logged out!"))
    return redirect("index")


