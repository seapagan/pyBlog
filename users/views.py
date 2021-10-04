"""Define views for the User App."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from blog.models import Blog
from users.forms import RegisterForm


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
    """View for the users profile page."""

    model = Blog
    template_name = "users/my_profile.html"
    context_object_name = "posts"
    paginate_by = 8  # show the last 8 posts

    def get_queryset(self):
        """Only get posts by this user."""
        queryset = super(MyProfileView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by(
            "-updated_at"
        )
        return queryset


class UserProfileView(DetailView):
    """View for a specific users profile page."""

    model = User
    template_name = "users/user-profile.html"
