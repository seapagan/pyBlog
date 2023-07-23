"""Test module for IndexClassView.""" ""
import pytest

import preferences
from blog.models import Blog
from blog.views.blog_views import IndexClassView


class TestIndexClassView:
    """Test class for IndexClassView."""

    blog_path = "/blog/"

    @pytest.mark.django_db
    def test_template_used(self, rf):
        """Test that the correct template is used."""
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        assert response.template_name == [
            "blog/index.html",
            "blog/blog_list.html",
        ]

    @pytest.mark.django_db
    def test_context_object_name(self, rf):
        """Test that the correct context object name is used."""
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        assert response.context_data["blogs"] is not None

    @pytest.mark.django_db
    def test_pagination(self, rf):
        """Test that pagination works as expected."""
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        assert len(response.context_data["blogs"]) == 6

    @pytest.mark.django_db
    def test_ordering(self, rf):
        """Test that the blogs are ordered by created_at in descending order."""
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        blogs = response.context_data["blogs"]
        for i in range(len(blogs) - 1):
            assert blogs[i].created_at >= blogs[i + 1].created_at

    @pytest.mark.django_db
    def test_page_title(self, rf):
        """Test that the page title is added to the context."""
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        assert (
            response.context_data["page_title"]
            == preferences.SitePreferences.heading
        )

    @pytest.mark.django_db
    def test_metadata(self, rf):
        """Test that the correct metadata is added to the context."""
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        meta = response.context_data["meta"]
        assert "twitter" in meta
        assert len(meta["twitter"]) == 4
        assert meta["twitter"][0]["name"] == "description"
        assert (
            meta["twitter"][0]["content"] == preferences.SitePreferences.heading
        )
        assert meta["twitter"][1]["name"] == "title"
        assert (
            meta["twitter"][1]["content"] == preferences.SitePreferences.title
        )
        assert meta["twitter"][2]["name"] == "site"
        assert (
            meta["twitter"][2]["content"]
            == f"@{preferences.SitePreferences.twitter_site}"
        )
        assert meta["twitter"][3]["name"] == "image"
        assert meta["twitter"][3]["content"] == request.build_absolute_uri(
            staticfiles_storage.url("blog/twitter.png")
        )

    @pytest.mark.django_db
    def test_no_blogs(self, rf):
        """Test that the view works when there are no blogs."""
        Blog.objects.all().delete()
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        assert len(response.context_data["blogs"]) == 0

    @pytest.mark.django_db
    def test_one_blog(self, rf):
        """Test that the view works when there is only one blog."""
        Blog.objects.all().delete()
        blog = Blog.objects.create(
            title="Test Blog", desc="Test Description", body="Test Body"
        )
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        assert len(response.context_data["blogs"]) == 1
        assert response.context_data["blogs"][0] == blog

    @pytest.mark.django_db
    def test_less_than_pagination_limit(self, rf):
        """Test the view works when there are < pagination limit of blogs."""
        Blog.objects.all().delete()
        for i in range(3):
            Blog.objects.create(
                title=f"Test Blog {i}",
                desc=f"Test Description {i}",
                body=f"Test Body {i}",
            )
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        assert len(response.context_data["blogs"]) == 3

    @pytest.mark.django_db
    def test_more_than_pagination_limit(self, rf):
        """Test the view works when there are > pagination limit of blogs."""
        Blog.objects.all().delete()
        for i in range(10):
            Blog.objects.create(
                title=f"Test Blog {i}",
                desc=f"Test Description {i}",
                body=f"Test Body {i}",
            )
        request = rf.get(self.blog_path)
        response = IndexClassView.as_view()(request)
        assert response.status_code == 200
        assert len(response.context_data["blogs"]) == 6

    @pytest.mark.django_db
    def test_invalid_page_number(self, rf):
        """Test the view returns a 404 error with invalid page number."""
        request = rf.get("/blog/?page=2")
        response = IndexClassView.as_view()(request)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_invalid_ordering_parameter(self, rf):
        """Test the view returns a 404 error with invalid ordering parameter."""
        request = rf.get("/blog/?ordering=invalid")
        response = IndexClassView.as_view()(request)
        assert response.status_code == 404
