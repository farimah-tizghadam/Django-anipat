from django.urls import include, path, reverse_lazy

from . import views
from django.contrib.auth import views as auth_views

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
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
        success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
        success_url=reverse_lazy("accounts:password_reset_complete"),

        ),
        name="password_reset_confirm",
    ),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
