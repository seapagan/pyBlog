"""Create the sitemap.xml file."""

from django.contrib.sitemaps import Sitemap
from django.urls.base import reverse

from blog.models import Blog


class StaticSiteMap(Sitemap):
    """Create the static sitemap."""

    changefreq = "daily"
    priority = 0.5

    def items(self):
        """Return the static items for the sitemap."""
        return ["latest-posts-feed"]

    def location(self, item):
        """Return the location of the static item."""
        return reverse(item)


class BlogSitemap(Sitemap):
    """Create the sitemap.xml file."""

    changefreq = "weekly"
    priority = 0.5

    def items(self):
        """Return all blog posts."""
        return Blog.objects.filter(draft=False)

    def lastmod(self, obj):
        """Return the last modified date."""
        return obj.updated_at

    def location(self, obj):
        """Return the location of the blog post."""
        return obj.get_absolute_url()
