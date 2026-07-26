from ...models import User, Profile
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import (
    RegistrationSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ResetConfirmSerializer,
    ActivationResendSerializer,
)

from mail_templated import EmailMessage
from ..utils import EmailThread
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .permissions import AllowUnauthenticatedUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        creating User via api
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data["email"]
        data = {"email": email}
        user = get_object_or_404(User, email=email)
        token = self.get_token_for_user(user)
        activation_path = reverse(
            "accounts:accounts-api-v1:activation",
            kwargs={"token": token},
        )

        activation_url = self.request.build_absolute_uri(activation_path)
        email_obj = EmailMessage(
            "email/activation.tpl",
            {
                "name": user.first_name or user.email,
                "token": token,
                "activation_url": activation_url,
            },
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        EmailThread(email_obj).start()
        return Response(data, status=status.HTTP_201_CREATED)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class UserVerificationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "email": request.user.email,
                "is_verified": request.user.is_verified,
            }
        )


class ActivationApiView(APIView):
    """
    Activating email
    """

    def get(self, request, token):
        # decode token in order to get user id
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "token is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"detail": "your account has been already verified"})
        user_obj.is_verified = True
        user_obj.save()

        return Response({"detail": "your account has been activated successfully"})
        # return Response(token)


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowUnauthenticatedUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage(
            "email/reset.tpl",
            {"token": token},
            "farimahtizghadam@gmail.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"detail": "check your email to reset your password"},
            status=status.HTTP_200_OK,
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "You should be logged out to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().handle_exception(exc)


class ConfirmResetPasswordApiView(generics.GenericAPIView):
    serializer_class = ResetConfirmSerializer
    permission_classes = [AllowUnauthenticatedUser]

    def put(self, request, token):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "token is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = User.objects.get(pk=user_id)
        user_obj.set_password(serializer.data.get("new_password"))
        user_obj.save()

        return Response({"detail": "your password has been reset successfully"})


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation.tpl",
            {"token": token},
            "farimahtizghadam@gmail.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"detail": "your activation resend successfully"}, status=status.HTTP_200_OK
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
