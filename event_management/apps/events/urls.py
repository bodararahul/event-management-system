"""Event routes."""

from __future__ import annotations

from django.urls import path

from apps.registrations.views import register_for_event
from .views import EventDetailView, EventListCreateView

urlpatterns = [
    path("", EventListCreateView.as_view(), name="event-list"),
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("<int:event_id>/register/", register_for_event, name="event-register"),
]
