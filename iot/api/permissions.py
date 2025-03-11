from rest_framework.permissions import BasePermission

from .models import APIKey


class HasValidAPIKey(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "auth") and isinstance(request.auth, APIKey)
