"""Settings to customize the overloaded Admin site."""

from django.contrib import admin


class MyAdminSite(admin.AdminSite):
    """Customize the Admin site strings."""

    site_header = "Blog Administration Panel"
    site_title = "Admin"
    index_title = "My Blog"
