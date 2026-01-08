"""Views for user authentication and profile."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.responses import error_response, success_response
from .serializers import LoginSerializer, ProfileSerializer, RegisterSerializer
from .services import generate_tokens_for_user, get_user_profile

User = get_user_model()


class RegisterView(APIView):
    """Handle user registration."""

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request) -> Response:
        """Create a new user."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = ProfileSerializer(user).data
            return success_response(data, "User registered", status.HTTP_201_CREATED)
        return error_response("Invalid data", errors=serializer.errors)


class LoginView(APIView):
    """Authenticate and return JWT tokens."""

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request) -> Response:
        """Authenticate user credentials."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = serializer.validated_data["tokens"]
            payload = {"user": ProfileSerializer(user).data, "tokens": tokens}
            return success_response(payload, "Login successful")
        return error_response(
            "Invalid credentials",
            errors=serializer.errors,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    """Simple stateless logout for JWT."""

    def post(self, request: Request) -> Response:
        """Return success; JWT invalidation handled client-side."""
        return success_response({}, "Logged out")


class ProfileView(APIView):
    """Return current user profile."""

    def get(self, request: Request) -> Response:
        """Return authenticated user's profile."""
        data = get_user_profile(request.user)
        return success_response(data)
