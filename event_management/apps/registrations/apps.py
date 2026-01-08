from __future__ import annotations

from django.apps import AppConfig


class RegistrationsConfig(AppConfig):
    """Registration app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.registrations"
    verbose_name = "Registrations"
