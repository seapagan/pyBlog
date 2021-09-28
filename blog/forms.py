"""Define any forms used in the Blogs app."""
from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):
    """Define the form to Add a comment."""

    class Meta:
        """Metadata for this form."""

        model = Comment

        fields = ("created_by_guest", "body")

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }
