"""Override some default http error handlers."""

from django.shortcuts import render
from django.template.loader import render_to_string
from maintenancemode import http
from preferences import preferences


def maintenance_mode(request, template_name="503.html"):
    """Create our own maintenance view, so we can add back the preferences."""
    context = {
        "request_path": request.path,
        "preferences": preferences,
    }

    return http.HttpResponseTemporaryUnavailable(
        render_to_string(template_name, context)
    )


def custom403(request, exception=None):
    """Create a custom 403 view, so we can add the page title context."""
    context = {"page_title": "Permission Denied!"}
    return render(request, "403.html", context, status=403)
    return


def custom404(request, exception=None):
    """Create a custom 404 view, so we can add the page title context."""
    context = {"page_title": "Not Found"}
    return render(request, "404.html", context, status=404)
