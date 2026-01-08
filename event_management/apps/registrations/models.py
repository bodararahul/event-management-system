"""Registration domain models."""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from common.constants import REGISTRATION_STATUS_ACTIVE, REGISTRATION_STATUS_CHOICES
from apps.events.models import Event


class Registration(models.Model):
    """Registration model linking users to events."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    registered_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS_CHOICES, default=REGISTRATION_STATUS_ACTIVE)

    class Meta:
        unique_together = ("user", "event")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["event"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        """Return readable representation."""
        return f"{self.user.email} -> {self.event.title}"

