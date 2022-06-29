"""Set up a Context Processor to add the preferences to the template context."""
from preferences import preferences


def preferences_cp(request):
    """Add preferences to template context.

    This allows use through TEMPLATE_CONTEXT_PROCESSORS setting.
    """
    return {"preferences": preferences}
