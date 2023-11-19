"""Define models used by the Users app."""
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models


class OverwriteStorage(FileSystemStorage):
    """Returns a filename that's free on the target storage system.

    Will delete any file with the same name.
    """

    def get_available_name(self, name, max_length=None):
        """Override the get_availiable_name, to delete existing file."""
        self.delete(name)
        super().get_available_name(name, max_length)
        return name


def get_upload_path(instance, filename):
    """Define a helper function to get a user-specific upload path."""
    ext = Path(filename).suffix
    filename = "avatar" + ext
    return Path("profile_pictures" / instance.user.username / filename)


class Profile(models.Model):
    """Define the Profile model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=get_upload_path,
        storage=OverwriteStorage(),
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

    def __str__(self) -> str:
        """Return the string representation of this model."""
        return self.user.username
