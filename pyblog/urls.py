"""Root URL Configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as authentication_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.feeds import PostsFeed
from blog.sitemaps import BlogSitemap, StaticSiteMap
from users import views as user_views

handler403 = "pyblog.errors.views.custom403"
handler404 = "pyblog.errors.views.custom404"

sitemaps = {"blog": BlogSitemap, "static": StaticSiteMap}

urlpatterns = (
    [  # noqa: RUF005
        path(
            "sitemap.xml",
            sitemap,
            {"sitemaps": sitemaps},
            name="django.contrib.sitemaps.views.sitemap",
        ),
        path("feed/posts/", PostsFeed(), name="latest-posts-feed"),
        path("", include("blog.urls")),
        path("register/", user_views.register, name="register"),
        path("login/", user_views.CustomLoginView.as_view(), name="login"),
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
        path(
            "profile/edit/",
            user_views.EditProfileView.as_view(),
            name="edit-profile",
        ),
        path("ckeditor/", include("ckeditor_uploader.urls")),
        path("likes/", include("likes.urls")),
        path("maintenance-mode/", include("maintenance_mode.urls")),
        path("", include("user_sessions.urls", "user_sessions")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

# only include the Admin paths if we are in DEBUG mode
if settings.DEBUG:
    urlpatterns = [  # noqa: RUF005
        path("admin/", admin.site.urls),
    ] + urlpatterns
