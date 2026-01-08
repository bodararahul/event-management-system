"""Service layer for event operations."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterable

from django.db import transaction
from django.db.models import Q, QuerySet
from django.utils import timezone

from common.constants import EVENT_STATUS_CHOICES, EVENT_STATUS_UPCOMING
from .models import Event


def validate_event_dates(start_date: datetime, end_date: datetime) -> None:
    """Ensure event start is before end."""
    if start_date >= end_date:
        raise ValueError("End date must be after start date")


def create_event(*, data: Dict[str, Any], created_by) -> Event:
    """Create a new event."""
    validate_event_dates(data["start_date"], data["end_date"])
    with transaction.atomic():
        event = Event.objects.create(created_by=created_by, **data)
    return event


def update_event(*, event: Event, data: Dict[str, Any]) -> Event:
    """Update an existing event."""
    if "start_date" in data and "end_date" in data:
        validate_event_dates(data["start_date"], data["end_date"])
    for field, value in data.items():
        setattr(event, field, value)
    event.updated_at = timezone.now()
    event.save()
    return event


def soft_delete_event(event: Event) -> None:
    """Soft delete an event."""
    event.delete()


def list_events(filters: Dict[str, Any]) -> QuerySet[Event]:
    """Return filtered events."""
    queryset = Event.objects.all()
    status = filters.get("status")
    if status:
        queryset = queryset.filter(status=status)
    location = filters.get("location")
    if location:
        queryset = queryset.filter(location__icontains=location)
    search = filters.get("search")
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    created_by = filters.get("created_by")
    if created_by:
        queryset = queryset.filter(created_by=created_by)
    start = filters.get("start_date")
    end = filters.get("end_date")
    if start and end:
        queryset = queryset.filter(start_date__gte=start, end_date__lte=end)
    return queryset


def get_event(event_id: int) -> Event:
    """Return event by id."""
    return Event.objects.get(pk=event_id)
