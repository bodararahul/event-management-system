"""Standardized API responses."""

from __future__ import annotations

from typing import Any, Optional

from rest_framework import status
from rest_framework.response import Response


def success_response(
    data: Any, message: str = "Success", status_code: int = status.HTTP_200_OK
) -> Response:
    """Return a standardized success response."""
    return Response(
        {"success": True, "message": message, "data": data}, status=status_code
    )


def error_response(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    errors: Optional[Any] = None,
) -> Response:
    """Return a standardized error response."""
    payload = {"success": False, "message": message}
    if errors is not None:
        payload["errors"] = errors
    return Response(payload, status=status_code)
