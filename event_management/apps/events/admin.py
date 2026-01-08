"""Admin registration for events."""

from __future__ import annotations

from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Event admin config."""

    list_display = (
        "title",
        "status",
        "start_date",
        "end_date",
        "capacity",
        "created_by",
        "is_deleted",
    )
    list_filter = ("status", "is_deleted")
    search_fields = ("title", "location")
    readonly_fields = ("created_at", "updated_at")
