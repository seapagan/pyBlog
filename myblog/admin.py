"""Settings to customise the overloaded Admin site."""
from django.contrib import admin


class MyAdminSite(admin.AdminSite):
    """Customise the Admin site strings."""

    site_header = "Blog Administration Panel"
    site_title = "Admin"
    index_title = "My Blog"
