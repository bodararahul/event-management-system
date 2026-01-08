"""Service layer for registration related logic."""

from __future__ import annotations

from typing import Any

from django.db import IntegrityError, transaction

from apps.events.models import Event
from apps.registrations.models import Registration
from apps.users.models import User
from common.constants import REGISTRATION_STATUS_ACTIVE


def register_user_for_event(user: User, event_id: int) -> Registration:
    """
    Register a user for an event.

    Args:
        user: The user to register
        event_id: The event ID to register for

    Returns:
        The created registration

    Raises:
        ValueError: If event not found, capacity exceeded, or duplicate registration
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist as exc:
        raise ValueError("Event not found") from exc

    # Check capacity
    current_registrations = Registration.objects.filter(
        event=event, status=REGISTRATION_STATUS_ACTIVE
    ).count()
    if current_registrations >= event.capacity:
        raise ValueError("Event capacity exceeded")

    # Check for existing registration
    if Registration.objects.filter(user=user, event=event).exists():
        raise ValueError("User already registered for this event")

    try:
        with transaction.atomic():
            registration = Registration.objects.create(
                user=user, event=event, status=REGISTRATION_STATUS_ACTIVE
            )
    except IntegrityError as exc:
        raise ValueError("Registration already exists") from exc

    return registration


def get_user_registrations(user: User) -> list[Registration]:
    """
    Get all registrations for a user.

    Args:
        user: The user to get registrations for

    Returns:
        List of registrations
    """
    return list(Registration.objects.filter(user=user).select_related("event"))


def get_all_registrations() -> list[Registration]:
    """
    Get all registrations (admin only).

    Returns:
        List of all registrations
    """
    return list(Registration.objects.select_related("user", "event").all())
