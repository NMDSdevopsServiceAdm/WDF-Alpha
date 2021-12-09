import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from alpha.learning_providers.models import LearningProvider


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, **options):
        self.stdout.write("Importing learning provider data...")

        r = requests.get("https://endorsement.skillsforcare.org.uk/providersdirectory")
        providers = r.json()
        for provider in providers:
            LearningProvider.objects.create(
                id=int(provider["Id"]), provider=provider["Provider"]
            )

        self.stdout.write("...Done")
