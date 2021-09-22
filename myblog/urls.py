"""Root URL Configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as authentication_views
from django.urls import include, path

from users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("register/", user_views.register, name="register"),
    path(
        "login/",
        authentication_views.LoginView.as_view(
            template_name="users/login.html"
        ),
        name="login",
    ),
    path(
        "logout/",
        authentication_views.LogoutView.as_view(
            template_name="users/logout.html"
        ),
        name="logout",
    ),
    # path("profile/", user_views.profilepage, name="profile"),
    path("profile/", user_views.ProfileView.as_view(), name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
