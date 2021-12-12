"""Configure RSS feeds for the Blog model."""
from django.contrib.syndication.views import Feed

from blog.models import Blog


class PostsFeed(Feed):
    """RSS feed for the blog posts."""

    title = "Tek:Cited Posts"
    link = "/"
    description = "Updates from Tek:Cited."

    def items(self):
        """Return the latest blog posts."""
        return Blog.objects.filter(draft=False).order_by("-created_at")[:5]

    def item_title(self, item):
        """Return the title of the blog post."""
        return item.title

    def item_description(self, item):
        """Return the description of the blog post."""
        return item.desc
