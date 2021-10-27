"""Root URL Configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as authentication_views
from django.urls import include, path

from users import views as user_views

urlpatterns = []
# only include the Admin paths if we are in DEBUG mode
if settings.DEBUG:
    urlpatterns += [path("admin/", admin.site.urls)]

handler503 = "myblog.views.maintenance_mode"

urlpatterns += (
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
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
