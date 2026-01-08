"""Tests for event models."""

from __future__ import annotations

import pytest
from django.utils import timezone
from datetime import timedelta

from apps.events.models import Event
from common.constants import EVENT_STATUS_UPCOMING


@pytest.mark.django_db
class TestEventModel:
    """Test cases for Event model."""

    def test_create_event(self, organizer_user) -> None:
        """Test creating an event."""
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            location="Test Location",
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=2),
            capacity=100,
            created_by=organizer_user,
        )
        assert event.title == "Test Event"
        assert event.status == EVENT_STATUS_UPCOMING
        assert event.is_deleted is False
        assert str(event) == "Test Event"

    def test_soft_delete_event(self, event) -> None:
        """Test soft deleting an event."""
        event_id = event.id
        event.delete()
        assert event.is_deleted is True
        # Event should not appear in default queryset
        assert not Event.objects.filter(id=event_id).exists()
        # But should exist in all_objects
        assert Event.all_objects.filter(id=event_id).exists()

    def test_event_active_queryset(self, event, organizer_user) -> None:
        """Test active queryset filters deleted events."""
        deleted_event = Event.objects.create(
            title="Deleted Event",
            description="Description",
            location="Location",
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=2),
            capacity=50,
            created_by=organizer_user,
            is_deleted=True,
        )
        active_events = Event.objects.all()
        assert event in active_events
        assert deleted_event not in active_events

