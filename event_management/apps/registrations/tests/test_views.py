"""Tests for registration views."""

from __future__ import annotations

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestRegistration:
    """Test cases for registration endpoints."""

    def test_register_for_event(self, authenticated_user_client, event, regular_user) -> None:
        """Test registering for an event."""
        response = authenticated_user_client.post(f"/api/events/{event.id}/register/")
        assert response.status_code == status.HTTP_200_OK
        assert "Successfully registered" in response.data["message"]

    def test_register_duplicate(self, authenticated_user_client, event, registration) -> None:
        """Test registering twice for same event fails."""
        response = authenticated_user_client.post(f"/api/events/{event.id}/register/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_capacity_exceeded(
        self, authenticated_user_client, event, organizer_user
    ) -> None:
        """Test registering when capacity is exceeded."""
        # Fill up the event capacity
        from apps.registrations.models import Registration
        from apps.users.models import User
        from common.constants import REGISTRATION_STATUS_ACTIVE

        for i in range(event.capacity):
            user = User.objects.create_user(
                email=f"user{i}@test.com", password="testpass123", name=f"User {i}"
            )
            Registration.objects.create(user=user, event=event, status=REGISTRATION_STATUS_ACTIVE)

        # Try to register one more
        response = authenticated_user_client.post(f"/api/events/{event.id}/register/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_unauthenticated(self, api_client, event) -> None:
        """Test unauthenticated user cannot register."""
        response = api_client.post(f"/api/events/{event.id}/register/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_my_registrations(self, authenticated_user_client, registration) -> None:
        """Test getting user's registrations."""
        response = authenticated_user_client.get("/api/registrations/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) >= 1

    def test_admin_get_all_registrations(
        self, authenticated_admin_client, registration
    ) -> None:
        """Test admin getting all registrations."""
        response = authenticated_admin_client.get("/api/admin/registrations/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) >= 1

    def test_user_cannot_get_all_registrations(
        self, authenticated_user_client, registration
    ) -> None:
        """Test regular user cannot get all registrations."""
        response = authenticated_user_client.get("/api/admin/registrations/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

