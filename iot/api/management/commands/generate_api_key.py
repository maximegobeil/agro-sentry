import secrets

from api.models import APIKey
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate a new API key for a station/device"

    def add_arguments(self, parser):
        parser.add_argument(
            "name", type=str, help="Name or identifier for the station/device"
        )

    def handle(self, *args, **options):
        name = options["name"]
        key = secrets.token_hex(32)  # 64 character hex string

        api_key = APIKey.objects.create(name=name, key=key)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created API key for {name}")
        )
        self.stdout.write(f"API Key: {key}")
