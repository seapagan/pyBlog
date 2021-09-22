"""Define models used by the Users app."""
import os

from django.contrib.auth.models import User
from django.db import models


def get_upload_path(instance, filename):
    return os.path.join("profile_pictures", instance.user.username, filename)


class Profile(models.Model):
    """Define the Profile model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        # default="default_profile_pic.png", upload_to="profile_pictures"
        default="default_profile_pic.png",
        upload_to=get_upload_path,
    )
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        """Return the string representation of this model."""
        return self.user.username
