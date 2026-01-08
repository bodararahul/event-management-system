"""Event domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from common.constants import EVENT_STATUS_CHOICES, EVENT_STATUS_UPCOMING


class EventQuerySet(models.QuerySet):
    """Custom queryset for soft delete support."""

    def active(self) -> "EventQuerySet":
        """Return only non-deleted events."""
        return self.filter(is_deleted=False)


class EventManager(models.Manager):
    """Manager ensuring soft-deleted events are hidden by default."""

    def get_queryset(self) -> EventQuerySet:  # type: ignore[override]
        """Return active queryset."""
        return EventQuerySet(self.model, using=self._db).active()


class Event(models.Model):
    """Event model."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=EVENT_STATUS_CHOICES,
        default=EVENT_STATUS_UPCOMING,
        db_index=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events"
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventManager()
    all_objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ["start_date"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["start_date", "end_date"]),
            models.Index(fields=["created_by"]),
        ]

    def delete(self, using=None, keep_parents=False) -> None:  # type: ignore[override]
        """Soft delete the event."""
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def __str__(self) -> str:
        """Return event title."""
        return self.title
