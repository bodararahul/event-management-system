"""Tests for registration models."""

from __future__ import annotations

import pytest

from apps.registrations.models import Registration
from common.constants import REGISTRATION_STATUS_ACTIVE


@pytest.mark.django_db
class TestRegistrationModel:
    """Test cases for Registration model."""

    def test_create_registration(self, regular_user, event) -> None:
        """Test creating a registration."""
        registration = Registration.objects.create(user=regular_user, event=event)
        assert registration.user == regular_user
        assert registration.event == event
        assert registration.status == REGISTRATION_STATUS_ACTIVE

    def test_registration_unique_together(self, regular_user, event) -> None:
        """Test that user cannot register twice for same event."""
        Registration.objects.create(user=regular_user, event=event)
        with pytest.raises(Exception):  # IntegrityError or ValidationError
            Registration.objects.create(user=regular_user, event=event)

    def test_registration_str(self, regular_user, event) -> None:
        """Test registration string representation."""
        registration = Registration.objects.create(user=regular_user, event=event)
        assert str(registration) == f"{regular_user.email} -> {event.title}"

