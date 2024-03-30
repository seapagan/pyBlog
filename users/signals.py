"""Signals for the User App."""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile


@receiver(post_save, sender=User)
def build_profile(sender, instance, created, **kwargs):  # noqa: ARG001
    """Build the profile object."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):  # noqa: ARG001
    """Save the profile."""
    instance.profile.save()
