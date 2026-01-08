"""Serializers for user operations."""

from __future__ import annotations

from typing import Any, Dict

from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.constants import ROLE_CHOICES
from . import services

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default=ROLE_CHOICES[-1][0])

    class Meta:
        model = User
        fields = ("email", "name", "password", "role")

    def create(self, validated_data: Dict[str, Any]) -> User:
        """Create user using service layer."""
        return services.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Serializer for login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate credentials."""
        user, tokens = services.authenticate_user(attrs["email"], attrs["password"])
        attrs["user"] = user
        attrs["tokens"] = tokens
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for profile detail."""

    class Meta:
        model = User
        fields = ("email", "name", "role", "date_joined")
