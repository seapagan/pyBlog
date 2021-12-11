"""Define any forms used in the Blogs app."""
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.forms.widgets import ClearableFileInput

from blog.models import Blog, Comment


class CustomImageField(ClearableFileInput):
    """Create our custom image upload widget."""

    template_name = "blog/widgets/clearable_file_input.html"
    initial_text = "Current Image"
    input_text = "Change Image"
    clear_checkbox_label = "Remove Image"
    # our own custom context variables.
    add_text_label = "Add an Image"
    show_initial = False

    def get_context(self, name, value, attrs):
        """Add our new variables to the context."""
        context = super().get_context(name, value, attrs)
        context["widget"].update(
            {
                "add_text_label": self.add_text_label,
                "show_initial": self.show_initial,
            }
        )
        return context


class NewCommentForm(forms.ModelForm):
    """Define the form to Add a comment."""

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        error_messages={
            "required": "Please tick the box to prove you are not a robot.",
        },
    )

    class Meta:
        """Metadata for this form."""

        model = Comment

        fields = ("created_by_guest", "guest_email", "body")

        labels = {
            "body": "Comment",
            "created_by_guest": "your name",
            "guest_email": "your email",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(NewCommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Overload the clean function to set validate comment fields."""
        super().clean()

        if self.user.is_authenticated:
            self.cleaned_data["created_by_guest"] = False
            self.cleaned_data["guest_email"] = ""
        else:
            if self.cleaned_data["created_by_guest"] == "":
                self.add_error("created_by_guest", "You must supply a Name.")
            if self.cleaned_data["guest_email"] == "":
                self.add_error("guest_email", "You must supply an email.")
        if self.cleaned_data["body"] == "":
            self.add_error("guest_email", "Please enter a comment!")

        return self.cleaned_data


class EditCommentForm(forms.ModelForm):
    """Define the form to Edit a comment."""

    class Meta:
        """Metadata for this form."""

        model = Comment

        fields = ("body",)
        labels = {
            "body": "",
        }


class NewPostForm(forms.ModelForm):
    """Define the form to Create a Post."""

    tags_list = forms.CharField(required=False, label="Tags")
    image = forms.ImageField(
        label="Post Header Image",
        widget=CustomImageField,
        required=False,
    )

    class Meta:
        """Metadata for this form."""

        model = Blog

        fields = (
            "title",
            "desc",
            "image",
            "body",
        )
        labels = {
            "title": "Post Title",
            "desc": "Post Description",
            "body": "",
            "image": "Post Header Image",
        }


class EditPostForm(forms.ModelForm):
    """Define the form to Edit a Post."""

    tags_list = forms.CharField(required=False, label="Tags")
    image = forms.ImageField(
        label="Post Header Image",
        widget=CustomImageField,
        required=False,
    )

    class Meta:
        """Metadata for this form."""

        model = Blog

        fields = ("title", "desc", "body", "image", "tags_list")
        labels = {
            "desc": "Description",
            "body": "",
        }
