"""Define models used by the Users app."""
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Define the Profile model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="default_profile_pic.png", upload_to="profile_pictures"
    )
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        """Return the string representation of this model."""
        return self.user.username
