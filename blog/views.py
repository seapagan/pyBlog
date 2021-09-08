"""Define the views for the 'blog' application."""
from django.views.generic import ListView

from blog.models import Blog


class IndexClassView(ListView):
    """Define a ListView for the index (Blog main page)."""

    model = Blog
    template_name = "blog/index.html"
    context_object_name = "blogs"
