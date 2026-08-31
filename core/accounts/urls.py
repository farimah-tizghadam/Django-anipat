from django.urls import include, path

from . import views

app_name = "accounts"


urlpatterns = [
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
    path("activation/<uidb64>/<token>/", views.activate_account, name="activate"),
    path(
        "profile/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path("", include("django.contrib.auth.urls")),
]
