"""Serializers for registration app."""

from __future__ import annotations

from rest_framework import serializers

from apps.events.serializers import EventSerializer
from apps.registrations.models import Registration
from apps.users.serializers import ProfileSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registration model."""

    user = ProfileSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True)

    class Meta:
        """Meta configuration."""

        model = Registration
        fields = ("id", "user", "event", "event_id", "registered_at", "status")
        read_only_fields = ("id", "user", "registered_at", "status")


class RegistrationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for registration lists."""

    event_title = serializers.CharField(source="event.title", read_only=True)
    event_location = serializers.CharField(source="event.location", read_only=True)
    event_start_date = serializers.DateTimeField(
        source="event.start_date", read_only=True
    )

    class Meta:
        """Meta configuration."""

        model = Registration
        fields = (
            "id",
            "event_title",
            "event_location",
            "event_start_date",
            "registered_at",
            "status",
        )
