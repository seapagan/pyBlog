"""Configure and customise the default Admin site."""
from django.contrib import admin

from blog.models import Blog


class BlogAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ["title", "created_at", "updated_at"]
    ordering = ("-created_at",)
    search_fields = ["title"]


admin.site.register(Blog, BlogAdmin)
