"""Define the Database models for this application."""
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from preferences.models import Preferences


class Blog(models.Model):
    """Define the blog model.

    This will contain individual blog entries.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name="blog_posts"
    )
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    slug = models.SlugField(default="", unique=True)

    class Meta:
        """Meta configuration for the Blog model."""

        ordering = ["-created_at"]

    def __str__(self):
        """Return string representation of the Blog object."""
        return self.title

    def save(self, *args, **kwargs):
        """Override the save fumction, so we can generate the slug."""
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Override get_absolute_url function."""
        return reverse("blog:detail", args=[self.slug])

    def no_of_comments(self):
        """Count comments on this post."""
        return Comment.objects.filter(related_post=self).count()


class Comment(models.Model):
    """Define the 'Comment' Model."""

    created_by_user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    created_by_guest = models.CharField(max_length=50, blank=True)
    related_post = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()

    def __str__(self):
        """Return string representation of the Blog object."""
        return (
            f"Comment by '{self.get_commenter()}' "
            f"on post: '{self.related_post}'"
        )

    def get_commenter(self):
        """Return either the logged in user name or temp user name."""
        return (
            self.created_by_user.username
            if self.created_by_user
            else self.created_by_guest
        )


class SitePreferences(Preferences):
    """Define the global site settings."""

    sitename = models.CharField(max_length=50, default="My Sexy Blog")
    title = models.CharField(max_length=20, default="My Blog")
    heading = models.CharField(
        max_length=200, default="A blog of blogging blogosity."
    )

    class Meta:
        """class-specific configuration."""

        verbose_name_plural = "Site Preferences"
