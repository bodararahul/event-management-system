"""Common permission classes."""

from __future__ import annotations

from rest_framework.permissions import BasePermission

from common.constants import ROLE_ADMIN, ROLE_ORGANIZER


class IsAdmin(BasePermission):
    """Allows access only to admin users."""

    def has_permission(self, request, view) -> bool:
        """Return True if user is admin."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == ROLE_ADMIN
        )


class IsOrganizer(BasePermission):
    """Allows access only to organizers."""

    def has_permission(self, request, view) -> bool:
        """Return True if user is organizer."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == ROLE_ORGANIZER
        )


class IsAdminOrOrganizer(BasePermission):
    """Allows access to admins or organizers."""

    def has_permission(self, request, view) -> bool:
        """Return True if user is admin or organizer."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {ROLE_ADMIN, ROLE_ORGANIZER}
        )
