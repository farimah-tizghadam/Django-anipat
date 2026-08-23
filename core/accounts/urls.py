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
        views.CustomLogoutView.as_view(),
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
