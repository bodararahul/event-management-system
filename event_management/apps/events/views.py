"""Event views."""

from __future__ import annotations

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from common.responses import success_response
from .filters import parse_event_filters
from .models import Event
from .permissions import EventPermission
from .serializers import EventSerializer
from .services import list_events, soft_delete_event


class EventListCreateView(generics.ListCreateAPIView):
    """List and create events."""

    serializer_class = EventSerializer
    permission_classes = [EventPermission]

    def get_queryset(self):
        """Return filtered queryset."""
        filters = parse_event_filters(self.request)
        return list_events(filters)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Override list to send standardized response."""
        response = super().list(request, *args, **kwargs)
        return success_response(
            response.data, "Events retrieved successfully", response.status_code
        )

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Override create to send standardized response."""
        response = super().create(request, *args, **kwargs)
        return success_response(
            response.data, "Event created successfully", status.HTTP_201_CREATED
        )


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an event."""

    serializer_class = EventSerializer
    permission_classes = [EventPermission]
    queryset = Event.objects.all()

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """Override retrieve to send standardized response."""
        response = super().retrieve(request, *args, **kwargs)
        return success_response(
            response.data, "Event retrieved successfully", response.status_code
        )

    def update(self, request: Request, *args, **kwargs) -> Response:
        """Override update to send standardized response."""
        response = super().update(request, *args, **kwargs)
        return success_response(
            response.data, "Event updated successfully", response.status_code
        )

    def perform_destroy(self, instance: Event) -> None:
        """Soft delete event."""
        soft_delete_event(instance)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Override delete to send standardized response."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response({}, "Event deleted", status.HTTP_200_OK)
