"""Serializers for events."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from rest_framework import serializers

from apps.users.serializers import ProfileSerializer
from common.constants import EVENT_STATUS_CHOICES
from . import services
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event CRUD."""

    status = serializers.ChoiceField(
        choices=EVENT_STATUS_CHOICES, default=EVENT_STATUS_CHOICES[0][0]
    )
    created_by = ProfileSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "location",
            "start_date",
            "end_date",
            "capacity",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_by", "created_at", "updated_at")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation."""
        start_date: datetime = attrs.get("start_date") or getattr(
            self.instance, "start_date", None
        )
        end_date: datetime = attrs.get("end_date") or getattr(
            self.instance, "end_date", None
        )
        if start_date and end_date:
            services.validate_event_dates(start_date, end_date)
        if attrs.get("capacity") is not None and attrs["capacity"] <= 0:
            raise serializers.ValidationError({"capacity": "Capacity must be positive"})
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Event:
        """Create event via service layer."""
        user = self.context["request"].user
        return services.create_event(data=validated_data, created_by=user)

    def update(self, instance: Event, validated_data: Dict[str, Any]) -> Event:
        """Update event via service layer."""
        return services.update_event(event=instance, data=validated_data)
