"""Configure and customise the default Admin site."""
from django.contrib import admin

from blog.models import Blog


class BlogAdmin(admin.ModelAdmin):
    """Define a custom admin class for the Blog model."""

    date_hierarchy = "created_at"
    list_display = ["title", "created_at", "updated_at", "slug"]
    ordering = ("-created_at",)
    search_fields = ["title"]
    readonly_fields = ["slug"]


admin.site.register(Blog, BlogAdmin)
