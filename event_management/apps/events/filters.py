"""Filtering helpers for events."""

from __future__ import annotations

from typing import Any, Dict

from django.utils.dateparse import parse_datetime
from rest_framework.request import Request


def parse_event_filters(request: Request) -> Dict[str, Any]:
    """
    Parse query params into filter dict.

    Supports:
    - status: Filter by event status
    - location: Filter by location (partial match)
    - search: Search in title and description
    - start_date/end_date: Date range filtering
    """
    filters: Dict[str, Any] = {}
    status = request.query_params.get("status")
    if status:
        filters["status"] = status
    location = request.query_params.get("location")
    if location:
        filters["location"] = location
    search = request.query_params.get("search")
    if search:
        filters["search"] = search
    created_by = request.query_params.get("created_by")
    if created_by:
        filters["created_by"] = created_by
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    if start_date and end_date:
        start = parse_datetime(start_date)
        end = parse_datetime(end_date)
        if start and end:
            filters["start_date"] = start
            filters["end_date"] = end
    return filters
