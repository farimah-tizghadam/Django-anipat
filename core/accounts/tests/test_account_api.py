import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


import jwt


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="testuser@test.com", password="@/$1234567", is_verified=True
    )
    return user


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def another_user():
    user = User.objects.create_user(
        email="another@test.com",
        password="@/$0987654",
        is_verified=False,
        is_active=True,
    )
    return user


@pytest.fixture
def get_valid_token(common_user):
    expiration_time = datetime.utcnow() + timedelta(
        seconds=settings.PASSWORD_RESET_TIMEOUT
    )
    token = {"user_id": common_user.id, "exp": expiration_time}
    return jwt.encode(token, settings.SECRET_KEY, algorithm="HS256")


@pytest.fixture
def get_token_for_user(common_user):
    refresh = RefreshToken.for_user(common_user)
    return str(refresh.access_token)


@pytest.mark.django_db
class TestUserApi:

    def test_registration_success_201_status_code(self, api_client, common_user):
        url = reverse("accounts:accounts-api-v1:registration")
        data = {
            "email": "newuser@test.com",
            "password": "@/1234567",
            "password_confirm": "@/1234567",
        }

        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_email_already_exist_400_status_code(self, api_client, common_user):
        url = reverse("accounts:accounts-api-v1:registration")
        data = {
            "email": "testuser@test.com",
            "password": "newpassword",
            "password_confirm": "newpassword",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_login_success_200_status_code(self, api_client, common_user):
        url = reverse("accounts:accounts-api-v1:token-login")
        data = {"email": "testuser@test.com", "password": "@/$1234567"}
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert "token" in response.data

    def test_login_invalid_400_status_code(self, api_client, common_user):
        url = reverse("accounts:accounts-api-v1:token-login")
        data = {}
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_logout_response_204_status_code(self, api_client, common_user):
        """
        get token from login in order to logout
        """

        url = reverse("accounts:accounts-api-v1:token-login")
        data = {"email": "testuser@test.com", "password": "@/$1234567"}
        login_response = api_client.post(url, data)
        token = login_response.data["token"]

        logout_url = reverse("accounts:accounts-api-v1:token-logout")
        api_client.credentials(HTTP_AUTHORIZATION="Token " + token)
        logout_response = api_client.post(logout_url)

        # Check for a successful logout response
        assert logout_response.status_code == 204

    def test_logout_response_401_status_code(self, api_client):
        url = reverse("accounts:accounts-api-v1:token-logout")
        response = api_client.post(url)
        assert response.status_code == 401

    def test_refresh_jwt_token_200_status_code(
        self,
        api_client,
        common_user,
    ):
        login_url = reverse("accounts:accounts-api-v1:jwt-create")

        login_response = api_client.post(
            login_url,
            {
                "email": common_user.email,
                "password": "@/$1234567",
            },
            format="json",
        )

        assert login_response.status_code == 200

        refresh_token = login_response.data["refresh"]

        refresh_url = reverse("accounts:accounts-api-v1:token-refresh")

        response = api_client.post(
            refresh_url,
            {"refresh": refresh_token},
            format="json",
        )

        assert response.status_code == 200

    def test_refresh_jwt_token_401_status_code(
        self,
        api_client,
    ):
        refresh_url = reverse("accounts:accounts-api-v1:token-refresh")

        response = api_client.post(
            refresh_url,
            {"refresh": "invalid-refresh-token"},
            format="json",
        )

        assert response.status_code == 401

    def test_refresh_jwt_token_400_status_code(
        self,
        api_client,
    ):
        refresh_url = reverse("accounts:accounts-api-v1:token-refresh")

        response = api_client.post(
            refresh_url,
            {},
            format="json",
        )

        assert response.status_code == 400

    def test_verify_jwt_token_200_status_code(
        self,
        api_client,
        common_user,
    ):
        login_url = reverse("accounts:accounts-api-v1:jwt-create")

        login_response = api_client.post(
            login_url,
            {
                "email": common_user.email,
                "password": "@/$1234567",
            },
            format="json",
        )

        assert login_response.status_code == 200

        access_token = login_response.data["access"]

        verify_url = reverse("accounts:accounts-api-v1:token-verify")

        response = api_client.post(
            verify_url,
            {"token": access_token},
            format="json",
        )

        assert response.status_code == 200
        assert response.data == {}

    def test_verify_jwt_token_400_status_code(
        self,
        api_client,
    ):
        verify_url = reverse("accounts:accounts-api-v1:token-verify")

        response = api_client.post(
            verify_url,
            {},
            format="json",
        )

        assert response.status_code == 400

    def test_change_password_success_200_status_code(
        self,
        api_client,
        common_user,
    ):
        url = reverse("accounts:accounts-api-v1:change-password")

        api_client.force_authenticate(user=common_user)

        response = api_client.put(
            url,
            {
                "old_password": "@/$1234567",
                "new_password": "@/$1234567//",
                "new_password_confirm": "@/$1234567//",
            },
            format="json",
        )

        assert response.status_code == 200

        common_user.refresh_from_db()

        assert common_user.check_password("@/$1234567//")

    def test_change_password_400_status_code(
        self,
        api_client,
        common_user,
    ):
        url = reverse("accounts:accounts-api-v1:change-password")

        api_client.force_authenticate(user=common_user)

        response = api_client.put(
            url,
            {
                "old_password": "@/$1234567",
                "new_password": "23",
                "new_password_confirm": "23",
            },
            format="json",
        )

        assert response.status_code == 400

    def test_change_password_requires_authentication(
        self,
        api_client,
    ):
        url = reverse("accounts:accounts-api-v1:change-password")

        response = api_client.put(
            url,
            {
                "old_password": "@/$1234567",
                "new_password": "@/$1234567//",
                "new_password_confirm": "@/$1234567//",
            },
            format="json",
        )

        assert response.status_code in (401, 403)

    def test_reset_password_200_status_code(
        self,
        api_client,
        common_user,
    ):
        url = reverse("accounts:accounts-api-v1:password_reset")

        response = api_client.post(
            url,
            {"email": common_user.email},
            format="json",
        )

        assert response.status_code == 200

    def test_reset_password_confirm_400_status_code(
        self,
        api_client,
        get_valid_token,
    ):
        url = reverse(
            "accounts:accounts-api-v1:" "password_reset_confirm",
            kwargs={
                "token": get_valid_token,
            },
        )

        response = api_client.put(
            url,
            {},
            format="json",
        )

        assert response.status_code == 400

    def test_activation_confirm_200_status_code(
        self,
        api_client,
        another_user,
    ):
        refresh = RefreshToken.for_user(another_user)
        token = str(refresh.access_token)

        url = reverse(
            "accounts:accounts-api-v1:activation",
            kwargs={
                "token": token,
            },
        )

        response = api_client.get(url)

        assert response.status_code == 200

        another_user.refresh_from_db()

        assert another_user.is_verified is True
