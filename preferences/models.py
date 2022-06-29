"""Define the preferences Models."""
from django.db import models
from django.dispatch import receiver

import preferences
from preferences.managers import SingletonManager


class Preferences(models.Model):
    """Define the preferences Model."""

    objects = models.Manager()
    singleton = SingletonManager()

    def __unicode__(self):
        """Return the unicode representation of the model."""
        return self._meta.verbose_name_plural.capitalize()

    __str__ = __unicode__

    class Meta:
        """Define the preferences Meta options."""

        abstract: True


@receiver(models.signals.class_prepared)
def preferences_class_prepared(sender, *args, **kwargs):
    """Add various preferences members to preferences.preferences.

    This enables easy access from code.
    """
    cls = sender
    if issubclass(cls, Preferences):
        # Add singleton manager to subclasses.
        cls.add_to_class("singleton", SingletonManager())
        # Add property for preferences object to preferences.preferences.
        setattr(
            preferences.Preferences,
            cls._meta.object_name,
            property(lambda x: cls.singleton.get()),
        )
