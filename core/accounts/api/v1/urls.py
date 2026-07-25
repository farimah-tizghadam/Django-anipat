from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


app_name = "accounts-api-v1"


urlpatterns = [
    path(
        "registration/",
        views.RegistrationAPIView.as_view(),
        name="registration",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),
    # jwt path
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "token/verify/",
        TokenVerifyView.as_view(),
        name="token-verify",
    ),
    path(
        "verification/",
        views.UserVerificationAPIView.as_view(),
        name="verification",
    ),
    # change password
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
      # reset password
    path(
        "password-reset/", views.ResetPasswordApiView.as_view(), name="password_reset"
    ),
    path(
        "password-reset/<str:token>",
        views.ConfirmResetPasswordApiView.as_view(),
        name="password_reset_confirm",
    ),
    # confirm user by email (user activation)
    path(
        "activation/confirm/<str:token>/",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # resend activation
    path(
        "activation/resend/",
        views.ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
        path(
        "profile/",
        views.ProfileAPIView.as_view(),
        name="profile",
    ),
]