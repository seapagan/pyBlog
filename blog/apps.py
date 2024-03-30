"""App configuration for blog app."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Specifies the configuration for the blog app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
