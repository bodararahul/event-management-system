"""Event permissions."""

from __future__ import annotations

from rest_framework.permissions import BasePermission, SAFE_METHODS

from common.constants import ROLE_ADMIN, ROLE_ORGANIZER


class EventPermission(BasePermission):
    """Allow read to authenticated users, writes to admin/organizer, delete admin only."""

    def has_permission(self, request, view) -> bool:
        """Check permission at request level."""
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        if request.method == "DELETE":
            return bool(request.user and request.user.role == ROLE_ADMIN)
        return bool(request.user and request.user.role in {ROLE_ADMIN, ROLE_ORGANIZER})

    def has_object_permission(self, request, view, obj) -> bool:
        """Apply same logic for object-level operations."""
        return self.has_permission(request, view)
