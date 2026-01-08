"""Pytest configuration and fixtures."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.events.models import Event
from apps.registrations.models import Registration
from common.constants import (
    EVENT_STATUS_UPCOMING,
    ROLE_ADMIN,
    ROLE_ORGANIZER,
    ROLE_USER,
)

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    """Return API client for testing."""
    return APIClient()


@pytest.fixture
def admin_user() -> User:
    """Create and return an admin user."""
    return User.objects.create_user(
        email="admin@test.com",
        password="testpass123",
        role=ROLE_ADMIN,
        name="Admin User",
    )


@pytest.fixture
def organizer_user() -> User:
    """Create and return an organizer user."""
    return User.objects.create_user(
        email="organizer@test.com",
        password="testpass123",
        role=ROLE_ORGANIZER,
        name="Organizer User",
    )


@pytest.fixture
def regular_user() -> User:
    """Create and return a regular user."""
    return User.objects.create_user(
        email="user@test.com",
        password="testpass123",
        role=ROLE_USER,
        name="Regular User",
    )


@pytest.fixture
def authenticated_admin_client(api_client: APIClient, admin_user: User) -> APIClient:
    """Return authenticated API client with admin user."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def authenticated_organizer_client(
    api_client: APIClient, organizer_user: User
) -> APIClient:
    """Return authenticated API client with organizer user."""
    api_client.force_authenticate(user=organizer_user)
    return api_client


@pytest.fixture
def authenticated_user_client(api_client: APIClient, regular_user: User) -> APIClient:
    """Return authenticated API client with regular user."""
    api_client.force_authenticate(user=regular_user)
    return api_client


@pytest.fixture
def event(organizer_user: User) -> Event:
    """Create and return a test event."""
    from django.utils import timezone
    from datetime import timedelta

    return Event.objects.create(
        title="Test Event",
        description="Test Description",
        location="Test Location",
        start_date=timezone.now() + timedelta(days=1),
        end_date=timezone.now() + timedelta(days=2),
        capacity=100,
        status=EVENT_STATUS_UPCOMING,
        created_by=organizer_user,
    )


@pytest.fixture
def registration(regular_user: User, event: Event) -> Registration:
    """Create and return a test registration."""
    return Registration.objects.create(user=regular_user, event=event)
