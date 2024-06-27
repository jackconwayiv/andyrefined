from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", include("social_django.urls")),
    path(
        "",
        RedirectView.as_view(pattern_name="react", permanent=True),
        name="index",
    ),
    path("logout/", login_required(views.logout), name="logout"),
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    path("check/", views.is_logged_in),
    path("unverified/", views.unverified, name="unverified"),
    re_path(r"^app/*", login_required(views.react), name="react"),
]
