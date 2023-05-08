"""Admin site configuration."""
from django.contrib.admin.apps import AdminConfig


class MyAdminConfig(AdminConfig):
    """Admin site configuration."""

    default_site = "pyblog.admin.MyAdminSite"
