"""Define the Database models for this application."""
from django.db import models


class Blog(models.Model):
    """Define the blog model.

    This will contain individual blog entries.
    """

    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()

    def __str__(self):
        """Return string representation of the Blog object."""
        return self.title
