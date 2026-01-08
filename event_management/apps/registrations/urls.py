"""URL configuration for registrations app."""

from __future__ import annotations

from django.urls import path

from apps.registrations import views

app_name = "registrations"

urlpatterns = [
    path("registrations/", views.my_registrations, name="my-registrations"),
    path("admin/registrations/", views.admin_registrations, name="admin-registrations"),
]
