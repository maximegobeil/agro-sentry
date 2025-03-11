from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get API key from header
        api_key_header = request.META.get("HTTP_X_API_KEY")
        if not api_key_header:
            return None

        try:
            api_key = APIKey.objects.get(key=api_key_header, is_active=True)

            api_key.last_used = timezone.now()
            api_key.save(update_fields=["last_used"])

            # Return (user, auth) tuple as required by DRF
            return (AnonymousUser(), api_key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")
