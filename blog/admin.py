"""Configure and customise the default Admin site."""
from django.contrib import admin
from django.db.models.functions import Lower
from preferences.admin import PreferencesAdmin

from blog.models import Blog, Comment, SitePreferences, Tag


class BlogAdmin(admin.ModelAdmin):
    """Define a custom admin class for the Blog model."""

    date_hierarchy = "created_at"
    list_display = ["title", "created_at", "updated_at", "slug", "user"]
    list_filter = ["created_at", "updated_at"]
    ordering = ("-created_at",)
    search_fields = ["title"]
    readonly_fields = ["slug"]


class CommentAdmin(admin.ModelAdmin):
    """Define a custom admin class for the Comment model."""

    list_display = ["__str__", "id", "created_at", "updated_at"]


class TagsAdmin(admin.ModelAdmin):
    """Define a custom admin class for the Tag Model."""

    list_display = ["tag_name", "pk", "tag_count", "tag_creator"]
    ordering = (Lower("tag_name"),)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(SitePreferences, PreferencesAdmin)
