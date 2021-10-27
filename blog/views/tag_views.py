"""Define the views for the Tag Model."""
from django.db.models.functions import Lower
from django.views.generic import DetailView, ListView

from blog.models import Blog, Tag


class TagDetailView(DetailView):
    """This will list all posts with a certain Tag slug."""

    model = Tag
    template_name = "blog/tag_detail.html"

    def get_context_data(self, **kwargs):
        """Add posts ant tags to this context, so we can use in the sidebar."""
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        context["page_title"] = f"Posts tagged as '{self.object.tag_name}'"

        return context


class TagListView(ListView):
    """List all the tags, and posts that are linked to them."""

    model = Tag
    template_name = "blog/tag/list.html"
    ordering = [Lower("tag_name")]

    def get_context_data(self, **kwargs):
        """Add posts ant tags to this context, so we can use in the sidebar."""
        context = super(TagListView, self).get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        context["page_title"] = "Tags"

        return context
