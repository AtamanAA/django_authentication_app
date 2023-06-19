from django.urls import path

from . import views


urlpatterns = [
    path("register_user/", views.register_user, name="register"),
    path("login_user/", views.login_user, name="login"),
    path("logout_user/", views.logout_user, name="logout"),
    # path("update_user/", views.update_user, name="update_user"),


    # path("", views.all_teachers, name="all_teachers"),
    # path("create/", views.create_teacher, name="create_teacher"),
    # path("<int:teacher_id>/", views.edit_teacher, name="edit_teacher"),
    # path("subject", views.all_subjects, name="all_subjects"),
    # path("create-subject/", views.create_subject, name="create_subject"),
    # path("subject/<int:subject_id>/", views.edit_subject, name="edit_subject"),

]
