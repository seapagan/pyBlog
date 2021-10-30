"""Root URL Configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as authentication_views
from django.urls import include, path

from users import views as user_views

handler503 = "myblog.errors.views.maintenance_mode"
handler403 = "myblog.errors.views.custom403"
handler404 = "myblog.errors.views.custom404"

urlpatterns = (
    [
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
        path(
            "profile/<int:pk>/",
            user_views.UserProfileView.as_view(),
            name="user-profile",
        ),
        path("profile/", user_views.MyProfileView.as_view(), name="my-profile"),
        path("ckeditor/", include("ckeditor_uploader.urls")),
        path("likes/", include("likes.urls")),
        path("maintenance-mode/", include("maintenance_mode.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

# only include the Admin paths if we are in DEBUG mode
if settings.DEBUG:
    urlpatterns = [path("admin/", admin.site.urls)] + urlpatterns
