import pytest
from django.urls import reverse
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User, Profile


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="testuser1@test.com",
        password="@/$1234567",
        is_verified=True,
        is_active=True,
    )

    Profile.objects.get_or_create(
        user=user,
    )

    return user


@pytest.mark.django_db
class TestPostApi:
    client = APIClient()

    def test_get_post_response_200_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "tst",
            "status": True,
            "content": "tst tst",
            "published": datetime.now(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_201_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        user = common_user
        api_client.force_authenticate(user=user)
        data = {
            "title": "tst",
            "status": True,
            "content": "tst tst",
            "published_date": datetime.now(),
            "tags": ["django", "drf", "pytest"],
        }

        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.data
