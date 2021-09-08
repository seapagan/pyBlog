"""Define the views for the 'blog' application."""
from django.views.generic import TemplateView

from blog.models import Blog


class IndexClassView(TemplateView):
    """Define a TemplateView for the index (Blog main page)."""

    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        """Return the context for this view.

        Doing it this way so as to enable multiple models to be shown in the
        template.
        """
        context = super(IndexClassView, self).get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all()
        return context
