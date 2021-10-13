"""Define URL patterns for the Blog app."""
from django.urls import path

from blog import views

app_name = "blog"
urlpatterns = [
    path("", views.IndexClassView.as_view(), name="index"),
    path("<str:slug>", views.PostDetailView.as_view(), name="detail"),
    path("new/", views.NewPostView.as_view(), name="add_post"),
    path(
        "<str:slug>/comment", views.AddCommentView.as_view(), name="add_comment"
    ),
    path("<str:slug>/edit", views.EditPostView.as_view(), name="edit_post"),
    path(
        "<str:slug>/delete", views.DeletePostView.as_view(), name="delete_post"
    ),
    path(
        "comment/<int:pk>/edit",
        views.EditCommentView.as_view(),
        name="edit_comment",
    ),
    path(
        "comment/<int:pk>/delete",
        views.DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    path("tags/<str:slug>/", views.TagDetailView.as_view(), name="tag_detail"),
]
