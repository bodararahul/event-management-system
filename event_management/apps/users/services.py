"""Service layer for user related logic."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction
from rest_framework_simplejwt.tokens import RefreshToken

from common.constants import ROLE_USER
from .models import User


def create_user(*, email: str, name: str, password: str, role: str = ROLE_USER) -> User:
    """Create a new user with hashed password."""
    try:
        with transaction.atomic():
            user = User.objects.create_user(
                email=email, name=name, password=password, role=role
            )
    except IntegrityError as exc:
        raise ValueError("Email already exists") from exc
    return user


def generate_tokens_for_user(user: User) -> Dict[str, str]:
    """Generate JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def authenticate_user(email: str, password: str) -> Tuple[User, Dict[str, str]]:
    """Authenticate user credentials and return user with tokens."""
    user = authenticate(email=email, password=password)
    if not user:
        raise ValueError("Invalid credentials")
    tokens = generate_tokens_for_user(user)
    return user, tokens


def get_user_profile(user: User) -> Dict[str, Any]:
    """Return user profile data."""
    return {
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "date_joined": user.date_joined,
    }
