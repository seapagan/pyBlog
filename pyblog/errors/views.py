"""Override some default http error handlers."""

from django.shortcuts import render


def custom403(request, exception=None):  # noqa: ARG001
    """Create a custom 403 view, so we can add the page title context."""
    context = {"page_title": "Permission Denied!"}
    return render(request, "403.html", context, status=403)


def custom404(request, exception=None):  # noqa: ARG001
    """Create a custom 404 view, so we can add the page title context."""
    context = {"page_title": "Not Found"}
    return render(request, "404.html", context, status=404)
