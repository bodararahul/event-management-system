"""Views for registration endpoints."""

from __future__ import annotations

from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.registrations.serializers import (
    RegistrationListSerializer,
    RegistrationSerializer,
)
from apps.registrations.services import (
    get_all_registrations,
    get_user_registrations,
    register_user_for_event,
)
from common.permissions import IsAdmin
from common.responses import error_response, success_response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_for_event(request: Request, event_id: int) -> Response:
    """
    Register the authenticated user for an event.

    Args:
        request: The HTTP request
        event_id: The event ID to register for

    Returns:
        Response with registration data or error
    """
    try:
        registration = register_user_for_event(request.user, event_id)
        serializer = RegistrationSerializer(registration)
        return success_response(serializer.data, "Successfully registered for event")
    except ValueError as exc:
        return error_response(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_registrations(request: Request) -> Response:
    """
    Get all registrations for the authenticated user.

    Args:
        request: The HTTP request

    Returns:
        Response with list of registrations
    """
    registrations = get_user_registrations(request.user)
    serializer = RegistrationListSerializer(registrations, many=True)
    return success_response(serializer.data, "Registrations retrieved successfully")


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdmin])
def admin_registrations(request: Request) -> Response:
    """
    Get all registrations (admin only).

    Args:
        request: The HTTP request

    Returns:
        Response with list of all registrations
    """
    registrations = get_all_registrations()
    serializer = RegistrationSerializer(registrations, many=True)
    return success_response(serializer.data, "All registrations retrieved successfully")
