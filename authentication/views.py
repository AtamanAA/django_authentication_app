from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from .models import Profile
from .forms import (
    RegisterUserForm,
    LoginUserForm,
    UpdateUserForm,
    PasswordChangeUserForm,
    ProfileUserForm,
)
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

                profile = Profile(user_id=user.id)
                profile.save()

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
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
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


def update_user(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            if (
                not User.objects.filter(username=username)
                or username == request.user.username
            ):
                user_form = UpdateUserForm(request.POST, instance=request.user)
                profile_form = ProfileUserForm(
                    request.POST, request.FILES, instance=request.user.profile
                )

                if user_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    profile_form.save()
                    login(
                        request,
                        request.user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                    messages.success(request, ("Your profile successfully updated!"))
                    return redirect("index")
                else:
                    messages.error(
                        request,
                        ("Invalid form. Try again!"),
                    )
                    return redirect("update")

            else:
                messages.error(
                    request,
                    (f"Username {username} is already in use! Choose another."),
                )
        else:
            if not Profile.objects.filter(user_id=request.user.id):
                profile = Profile(user_id=request.user.id)
                profile.save()

            user_form = UpdateUserForm(instance=request.user)
            profile_form = ProfileUserForm(instance=request.user.profile)
            context = {"user_form": user_form, "profile_form": profile_form}
            return render(request, "authentication/update_user.html", context)
    else:
        messages.error(request, ("You must register to access this page!"))
        return redirect("login")


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeUserForm(user=request.user, data=request.POST)
        old_password = request.POST["old_password"]
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("index")
        elif not request.user.check_password(old_password):
            messages.error(
                request,
                ("Your old password was entered incorrectly. Please enter it again."),
            )
        else:
            messages.error(
                request,
                (
                    "New password is incorect or the two new password fields didn’t match."
                ),
            )
        return redirect("change_password")

    else:
        form = PasswordChangeUserForm(request.user)
        return render(request, "authentication/change_password.html", {"form": form})


def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("index")
