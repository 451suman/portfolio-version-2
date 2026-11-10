
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("core.urls")),
    path("projects/", include("portfolio.urls")),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
    path("accounts/", include("accounts.urls")),

    # Redirect common URLs
    path(
        "home/",
        RedirectView.as_view(
            pattern_name="core:home",
            permanent=False
        )
    ),
    path(
        "about/",
        RedirectView.as_view(
            pattern_name="core:about",
            permanent=False
        )
    ),
    path(
        "portfolio/",
        RedirectView.as_view(
            pattern_name="portfolio:project_list",
            permanent=False
        )
    ),
]

# Serve media files during local development only
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
