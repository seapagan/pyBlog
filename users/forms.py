"""Custom forms for the users App."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """Custom form class for registering users."""

    email = forms.EmailField()

    class Meta:
        """Metadata for this class."""

        model = User
        fields = ["username", "email", "password1", "password2"]
