from django.contrib.auth.views import LogoutView
from django.urls import include, path

from . import views

app_name = "accounts"


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path(
        "login/",
        views.CustomLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(
            next_page="blog:post-list",
        ),
        name="logout",
    ),
    path(
        "register/",
        views.RegisterPageView.as_view(),
        name="register",
    ),
    path(
        "api/v1/",
        include("accounts.api.v1.urls", namespace="accounts-api-v1"),
    ),
]
