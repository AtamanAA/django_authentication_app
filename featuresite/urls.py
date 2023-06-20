from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),

    # path("auth_django/", include("django.contrib.auth.urls")),

]
