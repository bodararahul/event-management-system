"""Tests for user models."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from common.constants import ROLE_ADMIN, ROLE_ORGANIZER, ROLE_USER

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test cases for User model."""

    def test_create_user(self) -> None:
        """Test creating a regular user."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123", name="Test User"
        )
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == ROLE_USER
        assert user.check_password("testpass123")
        assert user.is_active is True

    def test_create_user_without_email(self) -> None:
        """Test creating user without email raises error."""
        with pytest.raises(ValueError, match="Users must have an email address"):
            User.objects.create_user(email="", password="testpass123")

    def test_create_superuser(self) -> None:
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123", name="Admin"
        )
        assert user.role == ROLE_ADMIN
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_user_str(self) -> None:
        """Test user string representation."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123", name="Test User"
        )
        assert str(user) == "test@example.com"

    def test_user_manager_create_user_with_role(self) -> None:
        """Test creating user with specific role."""
        user = User.objects.create_user(
            email="organizer@example.com",
            password="testpass123",
            name="Organizer",
            role=ROLE_ORGANIZER,
        )
        assert user.role == ROLE_ORGANIZER
