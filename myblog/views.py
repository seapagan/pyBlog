"""Override the maintenance mode 503 view."""

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
