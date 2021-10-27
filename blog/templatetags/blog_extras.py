"""Custom tag to remove draft posts in a template."""
from django import template
from django.db.models import Q
from django.db.models.functions import Lower

from blog.models import Blog, Tag

register = template.Library()


@register.filter()
def no_draft(tag_posts, user=None):
    """Filter draft posts out of the queryset."""
    # try to use the user (so we can see our own draft posts in the tag list),
    # if we get an exception then we are not logged in so it doesn't matter and
    # we just hide all draft posts
    try:
        filtered = tag_posts.exclude(Q(draft=True) & ~Q(user=user))
    except TypeError:
        filtered = tag_posts.exclude(draft=True)
    return filtered


# the below tag is used in the sidebar to pass extra context that is needed to
# get the sidebar to work.
@register.simple_tag
def sidebar():
    """Provide extra information needed for the sidebar"""
    context = {}
    context["posts"] = Blog.objects.all().order_by("-created_at")[:5]
    context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
    return context
