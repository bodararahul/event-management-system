"""Tests for event views."""

from __future__ import annotations

import pytest
from django.utils import timezone
from datetime import timedelta
from rest_framework import status

from apps.events.models import Event
from common.constants import EVENT_STATUS_UPCOMING


@pytest.mark.django_db
class TestEventListCreate:
    """Test cases for event list and create endpoints."""

    def test_list_events(self, api_client, event) -> None:
        """Test listing events."""
        response = api_client.get("/api/events/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1

    def test_create_event_as_admin(self, authenticated_admin_client, admin_user) -> None:
        """Test creating event as admin."""
        data = {
            "title": "New Event",
            "description": "Event Description",
            "location": "Event Location",
            "start_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=2)).isoformat(),
            "capacity": 50,
        }
        response = authenticated_admin_client.post("/api/events/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.filter(title="New Event").exists()

    def test_create_event_as_organizer(self, authenticated_organizer_client, organizer_user) -> None:
        """Test creating event as organizer."""
        data = {
            "title": "Organizer Event",
            "description": "Description",
            "location": "Location",
            "start_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=2)).isoformat(),
            "capacity": 30,
        }
        response = authenticated_organizer_client.post("/api/events/", data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_event_as_user_forbidden(self, authenticated_user_client) -> None:
        """Test regular user cannot create event."""
        data = {
            "title": "User Event",
            "description": "Description",
            "location": "Location",
            "start_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=2)).isoformat(),
            "capacity": 20,
        }
        response = authenticated_user_client.post("/api/events/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_event_unauthenticated(self, api_client) -> None:
        """Test unauthenticated user cannot create event."""
        data = {
            "title": "Public Event",
            "description": "Description",
            "location": "Location",
            "start_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=2)).isoformat(),
            "capacity": 10,
        }
        response = api_client.post("/api/events/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestEventDetail:
    """Test cases for event detail endpoint."""

    def test_get_event_detail(self, api_client, event) -> None:
        """Test getting event details."""
        response = api_client.get(f"/api/events/{event.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["title"] == event.title

    def test_update_event_as_organizer(self, authenticated_organizer_client, event) -> None:
        """Test updating event as organizer."""
        data = {"title": "Updated Title"}
        response = authenticated_organizer_client.patch(f"/api/events/{event.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        event.refresh_from_db()
        assert event.title == "Updated Title"

    def test_delete_event_as_admin(self, authenticated_admin_client, event) -> None:
        """Test deleting event as admin."""
        response = authenticated_admin_client.delete(f"/api/events/{event.id}/")
        assert response.status_code == status.HTTP_200_OK
        event.refresh_from_db()
        assert event.is_deleted is True

    def test_delete_event_as_organizer_forbidden(self, authenticated_organizer_client, event) -> None:
        """Test organizer cannot delete event."""
        response = authenticated_organizer_client.delete(f"/api/events/{event.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

