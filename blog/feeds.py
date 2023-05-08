"""Configure RSS feeds for the Blog model."""
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import DefaultFeed

from blog.models import Blog, Tag


class CorrectMimeTypeFeed(DefaultFeed):
    """Corrects the MIME type for the RSS feed."""

    content_type = "application/xml; charset=utf-8"


class PostsFeed(Feed):
    """RSS feed for the blog posts."""

    title = "Tek:Cited Posts"
    link = "/"
    description = "Updates from Tek:Cited."
    feed_copyright = "Copyright (c) 2021, Seapagan"
    feed_type = CorrectMimeTypeFeed

    def items(self):
        """Return the latest blog posts."""
        return Blog.objects.filter(draft=False).order_by("-created_at")[:5]

    def item_title(self, item):
        """Return the title of the blog post."""
        return item.title

    def item_description(self, item):
        """Return the description of the blog post."""
        return item.desc

    def item_author_name(self, item):
        """Return the author's name."""
        return item.user.username.capitalize()

    def item_pubdate(self, item):
        """Return the post's published date."""
        return item.created_at

    def item_updateddate(self, item):
        """Return the post's updated date."""
        return item.updated_at

    def item_categories(self, item):
        """Return the tags for this post as categories."""
        tags = Tag.objects.filter(posts=item)
        return list(tags.values_list("tag_name", flat=True))
