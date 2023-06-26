from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(
        upload_to="profile/photo",
        null=True,
        default="profile/photo/default_avatar.jpg",
    )
