"""Define the views for the 'blog' application."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

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
#     paginate_by = 6

#     def get_context_data(self, **kwargs):
#         """Return the context for this view.

#         Doing it this way (and not using a ListView so as to enable multiple
#         models to be shown in the template (eg comment counts etc).
#         """
#         context = super(IndexClassView, self).get_context_data(**kwargs)
#         context["blogs"] = Blog.objects.all().order_by("-created_at")

#         return context


class PostDetailView(DetailView):
    """Display an actual blog post."""

    model = Blog
    template = "blog/detail.html"


class NewPostView(LoginRequiredMixin, CreateView):
    """Add a new post to the Blog."""

    model = Blog
    fields = ["title", "desc", "body"]
    template_name = "blog/blog_newpost.html"

    def form_valid(self, form):
        """Validate the form."""
        form.instance.user = self.request.user
        print(self.request.user)

        return super().form_valid(form)
