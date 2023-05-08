"""Configure the Users App."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Specifies the configuration for the users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        """Import signals."""
        import users.signals  # noqa: F401
