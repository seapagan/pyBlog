"""Define models used by the Users app."""
import os

from django.contrib.auth.models import User
from django.db import models


def get_upload_path(instance, filename):
    """Helper function to get a user-specific upload path."""
    return os.path.join("profile_pictures", instance.user.username, filename)


class Profile(models.Model):
    """Define the Profile model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=get_upload_path,
    )
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True, default="")
    linkedin_user = models.CharField(max_length=50, blank=True, default="")
    facebook_user = models.CharField(max_length=50, blank=True, default="")
    github_user = models.CharField(max_length=50, blank=True, default="")
    youtube_user = models.CharField(max_length=50, blank=True, default="")
    twitter_user = models.CharField(max_length=50, blank=True, default="")
    bio = models.TextField(max_length=300, blank=True, default="")

    # set to true if the user can Author posts.
    author = models.BooleanField(default=False)

    def __str__(self):
        """Return the string representation of this model."""
        return self.user.username
