"""Define the views for the 'blog' application."""
from django.views.generic import DetailView, ListView

from blog.models import Blog


class IndexClassView(ListView):
    """Define a TemplateView for the index (Blog main page)."""

    template_name = "blog/index.html"
    context_object_name = "blogs"
    paginate_by = 6
    model = Blog


# class IndexClassView(TemplateView):
#     """Define a TemplateView for the index (Blog main page)."""

#     template_name = "blog/index.html"
#     paginate_by = 4

#     def get_context_data(self, **kwargs):
#         """Return the context for this view.

#         Doing it this way (and not using a ListView so as to enable multiple
#         models to be shown in the template.
#         """
#         context = super(IndexClassView, self).get_context_data(**kwargs)
#         context["blogs"] = Blog.objects.all()
#         return context


class PostDetailView(DetailView):
    """Display an actual blog post."""

    model = Blog
    template = "blog/detail.html"
