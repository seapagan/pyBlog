"""Define URL patterns for the Blog app."""
from django.urls import path

from blog import views

app_name = "blog"
urlpatterns = [path("", views.IndexClassView.as_view(), name="index")]
