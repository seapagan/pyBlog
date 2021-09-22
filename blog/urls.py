"""Define URL patterns for the Blog app."""
from django.urls import path

from blog import views

app_name = "blog"
urlpatterns = [
    path("", views.IndexClassView.as_view(), name="index"),
    path("<str:slug>", views.PostDetailView.as_view(), name="detail"),
    path("new/", views.NewPostView.as_view(), name="newpost"),
]
