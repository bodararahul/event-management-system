"""Tests for user views."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestRegistration:
    """Test cases for user registration."""

    def test_register_success(self, api_client) -> None:
        """Test successful user registration."""
        data = {
            "email": "newuser@test.com",
            "password": "testpass123",
            "name": "New User",
        }
        response = api_client.post("/api/auth/register/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data["data"]
        assert response.data["data"]["user"]["email"] == "newuser@test.com"
        assert User.objects.filter(email="newuser@test.com").exists()

    def test_register_duplicate_email(self, api_client) -> None:
        """Test registration with duplicate email fails."""
        User.objects.create_user(
            email="existing@test.com", password="testpass123", name="Existing"
        )
        data = {
            "email": "existing@test.com",
            "password": "testpass123",
            "name": "New User",
        }
        response = api_client.post("/api/auth/register/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_missing_fields(self, api_client) -> None:
        """Test registration with missing required fields."""
        data = {"email": "test@test.com"}
        response = api_client.post("/api/auth/register/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    """Test cases for user login."""

    def test_login_success(self, api_client, regular_user) -> None:
        """Test successful login."""
        data = {"email": "user@test.com", "password": "testpass123"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == status.HTTP_200_OK
        assert "tokens" in response.data["data"]
        assert "access" in response.data["data"]["tokens"]
        assert "refresh" in response.data["data"]["tokens"]

    def test_login_invalid_credentials(self, api_client) -> None:
        """Test login with invalid credentials."""
        data = {"email": "wrong@test.com", "password": "wrongpass"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_fields(self, api_client) -> None:
        """Test login with missing fields."""
        data = {"email": "test@test.com"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestProfile:
    """Test cases for user profile."""

    def test_get_profile_authenticated(self, authenticated_user_client, regular_user) -> None:
        """Test getting profile when authenticated."""
        response = authenticated_user_client.get("/api/auth/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["email"] == regular_user.email

    def test_get_profile_unauthenticated(self, api_client) -> None:
        """Test getting profile when not authenticated."""
        response = api_client.get("/api/auth/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

