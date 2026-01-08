"""User specific permissions."""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    """Allow access to the authenticated user's own profile."""

    def has_object_permission(self, request, view, obj) -> bool:
        """Return True when the object belongs to the user."""
        return obj == request.user
