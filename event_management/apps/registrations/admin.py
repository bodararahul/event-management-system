"""Admin registration for registrations."""

from __future__ import annotations

from django.contrib import admin

from apps.registrations.models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """Registration admin config."""

    list_display = ("user", "event", "registered_at", "status")
    list_filter = ("status", "registered_at")
    search_fields = ("user__email", "event__title")
    readonly_fields = ("registered_at",)
    date_hierarchy = "registered_at"
