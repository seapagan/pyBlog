"""Define the views for the Blog Model."""
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import Http404
from django.template.defaultfilters import slugify
from django.urls.base import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from hitcount.views import HitCountDetailView
from preferences import preferences

from blog.forms import EditPostForm, NewPostForm
from blog.models import Blog, Redirect, Tag

# from itertools import chain


class IndexClassView(ListView):
    """Define a TemplateView for the index (Blog main page)."""

    template_name = "blog/index.html"
    context_object_name = "blogs"
    paginate_by = 6
    ordering = ["-created_at"]
    model = Blog

    def get_context_data(self, **kwargs):
        """Add page title to the context."""
        context = super(IndexClassView, self).get_context_data(**kwargs)
        context["page_title"] = preferences.SitePreferences.heading
        # add description Metadata to the context
        context["meta"] = {
            "twitter": [
                {
                    "name": "description",
                    "content": preferences.SitePreferences.heading,
                },
                {
                    "name": "title",
                    "content": preferences.SitePreferences.title,
                },
                {
                    "name": "site",
                    "content": f"@{preferences.SitePreferences.twitter_site}",
                },
                {
                    "name": "image",
                    "content": self.request.build_absolute_uri(
                        staticfiles_storage.url("blog/twitter.png")
                    ),
                },
            ],
        }

        return context


class PostDetailView(HitCountDetailView):
    """Display an actual blog post."""

    model = Blog
    template = "blog/detail.html"
    count_hit = True

    def get_context_data(self, **kwargs):
        """Add page title to the context."""
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # set a custom page title for the post
        context["page_title"] = self.object.title.capitalize()
        # add description Metadata to the context
        context["meta"] = {
            "description": self.object.desc,
            "twitter": [
                {
                    "name": "description",
                    "content": self.object.desc,
                },
                {
                    "name": "title",
                    "content": self.object.title,
                },
                {"name": "creator", "content": f"@{self.object.user.username}"},
                {
                    "name": "site",
                    "content": f"@{preferences.SitePreferences.twitter_site}",
                },
            ],
        }
        # print(context)
        return context

    def get_object(self, queryset=None):
        """Get the correct post object.

        Return 404 if the post is a draft.
        If we have an old slug with a redirect value, go to the new slug.
        Return 404 if the slug is not found.
        """
        try:
            obj = super(PostDetailView, self).get_object()
        except Http404:
            slug_wanted = self.kwargs.get("slug")
            try:
                redirect = Redirect.objects.get(old_slug=slug_wanted)
            except Redirect.DoesNotExist:
                raise Http404("Post does not exist")
            obj = Blog.objects.get(pk=redirect.old_post_id)
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
        """Add page title to the context."""
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

        # get the original slug before any edits.
        original_slug = self.object.slug
        form.save()
        # if the slug has changed, add this to a redirect table
        new_slug = self.object.slug
        if (not original_slug == new_slug) and not self.object.draft:
            # the redirect may exist and should be unique, so we need to check
            # and update the existing in that case.
            try:
                redirect = Redirect.objects.get(old_slug=original_slug)
            except Redirect.DoesNotExist:
                # would be good in here to have logic to remove any surplus
                # redirect, for example when its redirected back to a previous
                # slug.
                redirect = Redirect(
                    old_slug=original_slug, old_post=self.object
                )
                redirect.save()

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
        """Add page title to the context."""
        context = super(EditPostView, self).get_context_data(**kwargs)
        context["page_title"] = self.object.title.capitalize()

        return context

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        post_slug = slugify(self.object.title)
        # post_slug = Blog.objects.get(slug=self.kwargs["slug"]).slug
        return reverse("blog:detail", kwargs={"slug": post_slug})

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the post.

        Also can edit if they are a superuser.
        """
        obj = super(EditPostView, self).get_object()

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
        """Add page title to the context."""
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


class SearchView(ListView):
    """Search for a post by title."""

    model = Blog
    template_name = "blog/blog_search.html"

    def get_queryset(self):
        """Search for a post by title and content."""
        query = self.request.GET.get("q")
        if query:
            blog_result = Blog.objects.filter(
                Q(title__icontains=query) | Q(desc__icontains=query)
            )
            # will want to include tag names in this search, but they need to
            # return posts not tags. Further work needed.
            # tag_result =Tag.objects.filter(tag_name__icontains=query)
            # object_list = chain(blog_result)
            object_list = blog_result
            return object_list

    def get_context_data(self, **kwargs):
        """Add page title to the context."""
        context = super(SearchView, self).get_context_data(**kwargs)
        context["page_title"] = "Search Results"
        context["query"] = self.request.GET.get("q")

        return context
