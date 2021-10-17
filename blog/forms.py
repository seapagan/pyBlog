"""Define any forms used in the Blogs app."""
from django import forms

from blog.models import Blog, Comment


class NewCommentForm(forms.ModelForm):
    """Define the form to Add a comment."""

    class Meta:
        """Metadata for this form."""

        model = Comment

        fields = ("created_by_guest", "body")

        labels = {
            "body": "",
        }


class NewPostForm(forms.ModelForm):
    """Define the form to Create a Post."""

    tags_list = forms.CharField(required=False, label="Tags")

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

    class Meta:
        """Metadata for this form."""

        model = Blog

        fields = ("desc", "body", "image", "tags_list")
        labels = {
            "desc": "Description",
            "body": "",
            "image": "Post Header Image",
        }


class EditCommentForm(forms.ModelForm):
    """Define the form to Edit a comment."""

    class Meta:
        """Metadata for this form."""

        model = Comment

        fields = ("body",)
        labels = {
            "body": "",
        }
