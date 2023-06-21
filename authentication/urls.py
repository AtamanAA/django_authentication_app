from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import PasswordResetUserForm, SetPasswordUserForm

urlpatterns = [
    path("register_user/", views.register_user, name="register"),
    path("login_user/", views.login_user, name="login"),
    path("logout_user/", views.logout_user, name="logout"),
    path("update_user/", views.update_user, name="update"),
    path("change_password/", views.change_password, name="change_password"),
    path(
        r"^activate/(?P<id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate,
        name="activate",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(form_class=PasswordResetUserForm),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(form_class=SetPasswordUserForm),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
