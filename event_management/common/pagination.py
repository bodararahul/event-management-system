"""Pagination helpers."""

from __future__ import annotations

from rest_framework.pagination import PageNumberPagination


class DefaultPageNumberPagination(PageNumberPagination):
    """Default pagination using page and page_size query params."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
