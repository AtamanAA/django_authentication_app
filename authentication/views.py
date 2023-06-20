from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from .forms import RegisterUserForm, LoginUserForm
from .tokens import account_activation_token


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            current_site = get_current_site(request)
            if User.objects.filter(email=email):
                messages.error(
                    request,
                    (f"Email {email} is already in use! Choose another."),
                )
                return render(request, "authentication/register.html", {"form": form})
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                message = render_to_string(
                    "authentication/account_activation_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "id": user.pk,
                        "token": account_activation_token.make_token(user),
                    },
                )
                user.email_user("Confirm registration", message)
                return render(
                    request,
                    "authentication/register_confirm_email.html",
                    {"email": email},
                )
    else:
        form = RegisterUserForm()
    return render(request, "authentication/register.html", {"form": form})


def activate(request, id, token):
    try:
        user = User.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, ("You have successfully registered!"))
        return redirect("index")
    else:
        return render(request, "authentication/account_activation_invalid.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            try:
                user_check = User.objects.filter(username=username).first()
                if not user_check.is_active:
                    messages.error(
                        request,
                        (
                            f"You email doesn't confirm! Please check {user_check.email} to complete registration."
                        ),
                    )
                    return redirect("login")
            except AttributeError:
                messages.error(
                    request, ("Username or password is incorrect, try again!")
                )
                return redirect("login")
    else:
        form = LoginUserForm()
        return render(request, "authentication/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, ("You logged out!"))
    return redirect("index")
