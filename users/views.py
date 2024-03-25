"""Define views for the User App."""

from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, UpdateView

from users.forms import EditProfileForm, LoginForm, RegisterForm
from users.models import Profile

ProfileContextType = dict[str, dict[str, str]]


def get_profile_context(profile_object) -> ProfileContextType:
    """Take the profile links and return a fuller dictionary."""
    my_profile = Profile.objects.filter(user=profile_object).values()[0]
    # remove certain fields that we dont want
    unwanted = ["id", "user_id", "user", "image", "location", "author", "bio"]
    my_copy = my_profile.copy()
    for item in my_copy:
        if item in unwanted:
            my_profile.pop(item)

    # lookup dictionary
    final = {
        "website": {
            "icon": "fal fa-globe",
            "base_url": "",
            "title": "Personal Website",
            "color": "var(--sidebar-links)",
        },
        "twitter_user": {
            "icon": "fab fa-twitter-square",
            "base_url": "https://twitter.com/",
            "title": "Twitter",
            "color": "#1DA1F2",
        },
        "github_user": {
            "icon": "fab fa-github-square",
            "base_url": "https://github.com/",
            "title": "GitHub Page",
            "color": "#333",
        },
        "youtube_user": {
            "icon": "fab fa-youtube-square",
            "base_url": "https://youtube.com/user/",
            "title": "Youtube Channel",
            "color": "#FF0000",
        },
        "linkedin_user": {
            "icon": "fab fa-linkedin",
            "base_url": "https://www.linkedin.com/in/",
            "title": "LinkedIn",
            "color": "#0077b5",
        },
        "facebook_user": {
            "icon": "fab fa-facebook-square",
            "base_url": "https://www.facebook.com/",
            "title": "Facebook",
            "color": "#4267B2",
        },
    }

    # add the link to the dictionary above.
    for item, value in my_profile.items():
        final[item]["value"] = value

    return final


def register(request: HttpRequest) -> HttpResponse:
    """Register a new user."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Welcome {username}, your account is created."
            )
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


class MyProfileView(LoginRequiredMixin, ListView):
    """View for the current users profile page."""

    template_name = "users/user-profile.html"
    context_object_name = "person"

    def get_queryset(self):
        """Customise the query to only return the logged in user."""
        return User.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        """Add links data to this context."""
        context = super().get_context_data(**kwargs)
        context["links"] = get_profile_context(self.object_list)
        context["page_title"] = self.object_list.username.capitalize()
        context["canonical"] = (
            f"{self.request.build_absolute_uri()}{self.request.user.pk}/"
        )
        return context


class UserProfileView(DetailView):
    """View for a specific users profile page."""

    model = User
    template_name = "users/user-profile.html"
    context_object_name = "person"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add links data to this context."""
        context = super().get_context_data(**kwargs)
        context["links"] = get_profile_context(self.object)
        context["page_title"] = self.object.username.capitalize()
        context["canonical"] = f"{self.request.build_absolute_uri()}"
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    """View for editing the current users profile."""

    form_class = EditProfileForm
    template_name = "users/edit-profile.html"
    success_url = "/profile/"
    context_object_name = "profile"

    def get_object(self):
        """Return the correct profile object."""
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add page_title to this context."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = (
            f"Editing Profile for {self.request.user.username.capitalize()}"
        )
        return context


class CustomLoginView(LoginView):
    """Custom login view."""

    template_name = "users/login.html"
    form_class = LoginForm
