"""Define the views for the Blog Model."""
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models.functions import Lower
from django.http import Http404
from django.urls.base import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from hitcount.views import HitCountDetailView
from preferences import preferences

from blog.forms import EditPostForm, NewPostForm
from blog.models import Blog, Tag


class IndexClassView(ListView):
    """Define a TemplateView for the index (Blog main page)."""

    template_name = "blog/index.html"
    context_object_name = "blogs"
    paginate_by = 6
    ordering = ["-created_at"]
    model = Blog

    def get_context_data(self, **kwargs):
        """Add tags to this context, so we can use in the sidebar."""
        context = super(IndexClassView, self).get_context_data(**kwargs)
        context["page_title"] = preferences.SitePreferences.heading

        return context


class PostDetailView(HitCountDetailView):
    """Display an actual blog post."""

    model = Blog
    template = "blog/detail.html"
    count_hit = True

    def get_context_data(self, **kwargs):
        """Add every post to this context, so we can use in the sidebar."""
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["page_title"] = self.object.title.capitalize()

        return context

    def get_object(self, queryset=None):
        """Return 404 if the post is a draft."""
        obj = super(PostDetailView, self).get_object()
        if obj.draft is True and self.request.user != obj.user:
            raise Http404("That Page does not exist")
        return obj


class NewPostView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Add a new post to the Blog."""

    model = Blog
    template_name = "blog/blog_newpost.html"
    form_class = NewPostForm

    def form_valid(self, form):
        """Validate the form."""
        form.save()
        tag_list = [
            tag.strip() for tag in form.cleaned_data["tags_list"].split(",")
        ]
        new_tags = []
        for tag in tag_list:
            if tag == "":
                continue
            try:
                existing_tag = Tag.objects.get(tag_name=tag.lower())
            except Tag.DoesNotExist:
                new_tags.append(
                    Tag.objects.create(
                        tag_name=tag.lower(), tag_creator=self.request.user
                    )
                )
            else:
                new_tags.append(existing_tag)

        # replace all the tag associations on this post with the new list
        form.instance.tag_set.set(new_tags)

        # detect if we want this a draft or not.
        if "draft" in self.request.POST:
            form.instance.draft = True

        # make sure we have the correct user tagged to this post
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add every post and tag to context, so we can use in the sidebar."""
        context = super(NewPostView, self).get_context_data(**kwargs)
        context["page_title"] = "New Post"

        return context

    def test_func(self):
        """Determine if we have the author permission or are superuser."""
        return (
            self.request.user.profile.author or self.request.user.is_superuser
        )


class EditPostView(LoginRequiredMixin, UpdateView):
    """Edit an existing Post."""

    model = Blog
    form_class = EditPostForm
    template_name = "blog/blog_editpost.html"

    def form_valid(self, form):
        """Validate the form."""
        form.save()
        tag_list = [
            tag.strip() for tag in form.cleaned_data["tags_list"].split(",")
        ]

        new_tags = []
        for tag in tag_list:
            if tag == "":
                continue
            try:
                existing_tag = Tag.objects.get(tag_name=tag.lower())
            except Tag.DoesNotExist:
                new_tags.append(
                    Tag.objects.create(
                        tag_name=tag.lower(), tag_creator=self.request.user
                    )
                )
            else:
                new_tags.append(existing_tag)

        form.instance.tag_set.set(new_tags)

        if "publish" in self.request.POST:
            # turn off the draft flag
            form.instance.draft = False
            # zero page view count
            form.instance.hit_count_generic.clear()
            # reset the created_at and updated_at time to right now
            form.instance.created_at = datetime.now()
            form.instance.updated_at = datetime.now()

        return super().form_valid(form)

    def get_initial(self):
        """Override initial value to display active tags."""
        initial = super(EditPostView, self).get_initial()

        current_tags = self.object.tag_set.all().order_by(Lower("tag_name"))
        tag_string = ""
        for tag in current_tags:
            tag_string += tag.tag_name + ", "
        initial["tags_list"] = tag_string[:-2]

        return initial

    def get_context_data(self, **kwargs):
        """Add every post and tag to context, so we can use in the sidebar."""
        context = super(EditPostView, self).get_context_data(**kwargs)
        context["page_title"] = self.object.title.capitalize()

        return context

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        post_slug = Blog.objects.get(slug=self.kwargs["slug"]).slug
        return reverse("blog:detail", kwargs={"slug": post_slug})

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the post.

        Also can edit if they are a superuser.
        """
        obj = super(EditPostView, self).get_object()
        # if obj.user == self.request.user or self.request.user.is_superuser:
        #     return obj

        if (
            obj.user == self.request.user and self.request.user.profile.author
        ) or self.request.user.is_superuser:
            return obj

        raise PermissionDenied


class DeletePostView(LoginRequiredMixin, DeleteView):
    """Edit an existing Post."""

    model = Blog
    # template_name = "blog/blog_deletepost.html"

    success_url = reverse_lazy("blog:index")

    def get_context_data(self, **kwargs):
        """Add every post to this context, so we can use in the sidebar."""
        context = super(DeletePostView, self).get_context_data(**kwargs)
        context["page_title"] = self.object.title.capitalize()

        return context

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the post.

        They must also still be tagged as an Author in their profile.
        Also can delete if they are a superuser.
        """
        obj = super(DeletePostView, self).get_object()
        if (
            obj.user == self.request.user and self.request.user.profile.author
        ) or self.request.user.is_superuser:
            return obj

        raise PermissionDenied
