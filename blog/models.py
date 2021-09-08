"""Define the Database models for this application."""
from django.db import models
from django.template.defaultfilters import slugify


class Blog(models.Model):
    """Define the blog model.

    This will contain individual blog entries.
    """

    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    slug = models.SlugField(default="")

    def __str__(self):
        """Return string representation of the Blog object."""
        return self.title

    def save(self, *args, **kwargs):
        """Override the save fumction, so we can generate the slug."""
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)
