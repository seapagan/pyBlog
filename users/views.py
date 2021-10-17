"""Define views for the User App."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from blog.models import Blog, Tag
from users.forms import RegisterForm
from users.models import Profile


def get_profile_context(profile_object):
    """Take the profile links and return a fuller dictionary."""
    my_profile = Profile.objects.filter(user=profile_object).values()[0]
    # remove certain fields that we dont want
    unwanted = ["id", "user_id", "user", "image", "location"]
    my_copy = my_profile.copy()
    for item in my_copy:
        if item in unwanted:
            my_profile.pop(item)

    # lookup dictionary
    final = {
        "website": {
            "icon": "fal fa-globe",
            "base_url": "",
            "title": "Homepage",
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

    # add the link to the disctionary above.
    for item, value in my_profile.items():
        final[item]["value"] = value

    return final


# Create your views here.
def register(request):
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

    # model = User
    template_name = "users/user-profile.html"
    context_object_name = "person"

    def get_queryset(self):
        """Customise the query to only return the logged in user."""
        return User.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        """Add links data to this context."""
        context = super(MyProfileView, self).get_context_data(**kwargs)
        context["links"] = get_profile_context(self.object_list)
        context["page_title"] = self.object_list.username.capitalize()
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        return context


class UserProfileView(DetailView):
    """View for a specific users profile page."""

    model = User
    template_name = "users/user-profile.html"
    context_object_name = "person"

    def get_context_data(self, **kwargs):
        """Add links data to this context."""
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context["links"] = get_profile_context(self.object)
        context["page_title"] = self.object.username.capitalize()
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        return context
