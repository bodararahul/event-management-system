"""User model definitions."""

from __future__ import annotations

from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from common.constants import ROLE_ADMIN, ROLE_CHOICES, ROLE_USER


class UserManager(BaseUserManager):
    """Custom user manager using email as username."""

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "User":
        """Create and return a regular user."""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str, **extra_fields: Any
    ) -> "User":
        """Create and return a superuser."""
        extra_fields.setdefault("role", ROLE_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("role") != ROLE_ADMIN:
            raise ValueError("Superuser must have role ADMIN")
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=ROLE_USER, db_index=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
        ]
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        """Return string representation."""
        return self.email
