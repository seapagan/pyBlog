"""Custom tag to remove draft posts in a template."""
from django import template

register = template.Library()


@register.filter()
def no_draft(tag_posts):
    """Filter draft posts out of the queryset."""
    filtered = tag_posts.exclude(draft=True)

    return filtered
