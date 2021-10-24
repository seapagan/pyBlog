"""Define the views for the 'blog' application."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.http.response import Http404
from django.urls.base import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from preferences import preferences

from blog.forms import (
    EditCommentForm,
    EditPostForm,
    NewCommentForm,
    NewPostForm,
)
from blog.models import Blog, Comment, Tag


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
        context["tags"] = Tag.objects.all().order_by("tag_name")
        context["page_title"] = preferences.SitePreferences.heading

        return context


class PostDetailView(DetailView):
    """Display an actual blog post."""

    model = Blog
    template = "blog/detail.html"

    def get_context_data(self, **kwargs):
        """Add every post to this context, so we can use in the sidebar."""
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # below are required to get the sidebar working
        context["blogs"] = (
            Blog.objects.all().exclude(draft=True).order_by("-created_at")
        )
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        # add post name to the page TITLE tag
        context["page_title"] = self.object.title.capitalize()

        return context

    def get_object(self, queryset=None):
        """Return 404 if the post is a draft."""
        obj = super(PostDetailView, self).get_object()
        if obj.draft is True:
            raise Http404("That Page does not exist")
        return obj


class NewPostView(LoginRequiredMixin, CreateView):
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
            print("This will be a draft")
            form.instance.draft = True
        else:
            print("This is getting published")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add every post and tag to context, so we can use in the sidebar."""
        context = super(NewPostView, self).get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        context["page_title"] = "New Post"

        return context


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
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
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
        if (
            not obj.user == self.request.user
            and not self.request.user.is_superuser
        ):
            raise Http404("You Dont have permission to do that!")
        return obj


class DeletePostView(LoginRequiredMixin, DeleteView):
    """Edit an existing Post."""

    model = Blog
    # template_name = "blog/blog_deletepost.html"

    success_url = reverse_lazy("blog:index")

    def get_context_data(self, **kwargs):
        """Add every post to this context, so we can use in the sidebar."""
        context = super(DeletePostView, self).get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        context["page_title"] = self.object.title.capitalize()

        return context

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the post.

        Also can delete if they are a superuser.
        """
        obj = super(DeletePostView, self).get_object()
        if (
            not obj.user == self.request.user
            and not self.request.user.is_superuser
        ):
            raise Http404("You Dont have permission to do that!")
        return obj


class AddCommentView(CreateView):
    """Add a new comment to a specific post."""

    model = Comment
    form_class = NewCommentForm
    template_name = "blog/comment_newcomment.html"

    def get_context_data(self, **kwargs):
        """Add extra context to the View.

        This allows us to access Post-related stuff like the title from inside
        our view.
        """
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        context["post"] = Blog.objects.get(slug=slug)
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        context["form"].related_post = context["post"]
        context["page_title"] = "New Comment"

        return context

    def form_valid(self, form):
        """Validate the form."""
        form.instance.related_post_id = Blog.objects.get(
            slug=self.kwargs["slug"]
        ).id
        if self.request.user:
            form.instance.created_by_user_id = self.request.user.id
        # else:
        #     form.instance.created_by_guest = "Guest User"

        return super().form_valid(form)

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        return reverse("blog:detail", kwargs={"slug": self.kwargs["slug"]})


class EditCommentView(LoginRequiredMixin, UpdateView):
    """Edit an existing comment ."""

    model = Comment
    form_class = EditCommentForm
    template_name = "blog/comment_editcomment.html"

    def get_context_data(self, **kwargs):
        """Add extra context to the View.

        This allows us to access Post-related stuff like the title from inside
        our view.
        """
        context = super().get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        context["page_title"] = "Edit Comment"

        return context

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        post_slug = Comment.objects.get(pk=self.kwargs["pk"]).related_post.slug
        return reverse("blog:detail", kwargs={"slug": post_slug})

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the comment."""
        obj = super(EditCommentView, self).get_object()
        if (
            not obj.created_by_user == self.request.user
            and not self.request.user.is_superuser
        ):
            raise Http404("You Dont have permission to do that!")
        return obj


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    """Delete an existing comment."""

    model = Comment

    def get_success_url(self) -> str:
        """On success, return to the blog post we commented on."""
        post_slug = Comment.objects.get(pk=self.kwargs["pk"]).related_post.slug
        return reverse("blog:detail", kwargs={"slug": post_slug})

    def get_object(self, queryset=None):
        """Ensure that the current logged in user owns the comment."""
        obj = super(DeleteCommentView, self).get_object()
        if (
            not obj.created_by_user == self.request.user
            and not self.request.user.is_superuser
        ):
            raise Http404("You Dont have permission to do that!")
        return obj


class TagDetailView(DetailView):
    """This will list all posts with a certain Tag slug."""

    model = Tag
    template_name = "blog/tag_detail.html"

    def get_context_data(self, **kwargs):
        """Add posts ant tags to this context, so we can use in the sidebar."""
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        context["page_title"] = f"Posts tagged as '{self.object.tag_name}'"

        return context


class TagListView(ListView):
    """List all the tags, and posts that are linked to them."""

    model = Tag
    template_name = "blog/tag/list.html"
    ordering = [Lower("tag_name")]

    def get_context_data(self, **kwargs):
        """Add posts ant tags to this context, so we can use in the sidebar."""
        context = super(TagListView, self).get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all().order_by("-created_at")
        context["tags"] = Tag.objects.all().order_by(Lower("tag_name"))
        context["page_title"] = "Tags"

        return context
