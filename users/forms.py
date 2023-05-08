"""Custom forms for the users App."""
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput, TextInput

from myblog.widgets.image import CustomImageField
from users.models import Profile


class LoginForm(AuthenticationForm):
    """Custom Login Form."""

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        error_messages={
            "required": "Please tick the box to prove you are not a robot.",
        },
    )

    class Meta:
        """Metadata for this class.

        Remove the label for the captcha field.
        """

        labels = {
            "captcha": "",
        }


class RegisterForm(UserCreationForm):
    """Custom form class for registering users."""

    email = forms.EmailField()

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        error_messages={
            "required": "Please tick the box to prove you are not a robot.",
        },
    )

    def __init__(self, *args, **kwargs):
        """Customize the registration form labels."""
        super().__init__(*args, **kwargs)

        self.fields["username"].widget = TextInput(
            attrs={
                "placeholder": "Choose a Username",
                "class": "form-control",
            }
        )
        self.fields["email"].widget = TextInput(
            attrs={
                "placeholder": "Enter a valid Email",
                "class": "form-control",
            }
        )

        self.fields["password1"].label = "Password"
        self.fields["password1"].widget = PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            }
        )
        self.fields["password2"].label = ""
        self.fields["password2"].widget = PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
            }
        )
        self.fields["captcha"].label = ""

    class Meta:
        """Metadata for this class."""

        model = User
        fields = ["username", "email"]


class EditProfileForm(forms.ModelForm):
    """Define the form to Edit a Profile."""

    image = forms.ImageField(
        label="Avatar",
        widget=CustomImageField,
        required=True,
    )

    class Meta:
        """Metadata for this form."""

        model = Profile
        fields = [
            "location",
            "bio",
            "image",
            "website",
            "linkedin_user",
            "facebook_user",
            "github_user",
            "youtube_user",
            "twitter_user",
        ]
