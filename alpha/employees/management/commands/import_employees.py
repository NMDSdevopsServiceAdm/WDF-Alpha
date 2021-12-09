import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from alpha.employees.models import Employee


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.data_path = Path(settings.BASE_DIR) / "alpha" / "employees" / "data"
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def handle(self, **options):
        self.stdout.write("Importing fake employees data...")

        with open(self.data_path / "fake_people.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Employee.objects.create(
                    name=row["name"],
                    workplace=row["workplace"],
                    job_role=row["job_role"],
                )

        self.stdout.write("...Done")
