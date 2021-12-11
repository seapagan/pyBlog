"""Create the sitemap.xml file."""
from django.contrib.sitemaps import Sitemap

from blog.models import Blog


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
