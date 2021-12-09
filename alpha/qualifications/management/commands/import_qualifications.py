import csv
import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from alpha.qualifications.models import (
    AwardingBody,
    FundingYear,
    Qualification,
    QualificationValue,
)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.data_path = Path(settings.BASE_DIR) / "alpha" / "qualifications" / "data"
        super().__init__(*args, **kwargs)

    def _clean_csv(self, filename):
        with open(self.data_path / filename) as csvfile:
            reader = csv.DictReader(csvfile)
            rows = []
            for row in reader:
                for k, _ in row.items():
                    if row[k] == "NULL":
                        row[k] = None
                rows.append(row)
        return rows

    def _parse_timestemp(self, timestamp):
        if not timestamp:
            return timestamp
        dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt

    def _get_qualification_category(self, row):
        if bool(int(row["IsPartOfApprenticeship"])):
            return "Apprenticeship"
        if "/" in row["QualificationCode"]:
            return "Qualification"
        if row["QualificationCode"].startswith("DL"):
            return "Digital Learning Module"
        return "Learning Programme"

    def _get_qualification_type(self, row):
        if "Award" in row["QualificationType"]:
            return "Award"
        if "Certificate" in row["QualificationType"]:
            return "Certificate"
        if "Diploma" in row["QualificationTitle"]:
            return "Diploma"
        return ""

    def _import_funding_years(self):
        rows = self._clean_csv("funding_years.csv")
        for row in rows:
            FundingYear.objects.create(
                id=row["FundingYearId"],
                year_code=row["YearCode"],
                description=row["Description"],
                is_deleted=bool(int(row["IsDeleted"])),
                created_date=self._parse_timestemp(row["CreatedDate"]),
                last_updated_date=self._parse_timestemp(row["LastUpdatedDate"]),
            )

    def _import_awarding_bodies(self):
        rows = self._clean_csv("awarding_bodies.csv")
        for row in rows:
            AwardingBody.objects.create(
                id=row["AwardingBodyId"],
                name=row["Name"],
                is_deleted=bool(int(row["IsDeleted"])),
                created_date=self._parse_timestemp(row["CreatedDate"]),
                last_updated_date=self._parse_timestemp(row["LastUpdatedDate"]),
            )

    def _import_qualifications(self):
        rows = self._clean_csv("qualifications.csv")
        for row in rows:
            qualification_category = self._get_qualification_category(row)
            qualification_type1 = self._get_qualification_type(row)

            Qualification.objects.create(
                id=row["QualificationId"],
                qualification_code=row["QualificationCode"],
                qualification_title=row["QualificationTitle"],
                qualification_type2=row["QualificationType"],
                awarding_body_id=row["AwardingBodyId"],
                level=row["Level"],
                num_credits=row["Credits"],
                is_part_of_apprenticeship=bool(int(row["IsPartOfApprenticeship"])),
                is_pre_funded=bool(int(row["IsPreFunded"])),
                is_endpoint_assesement=bool(int(row["IsEndPointAssesement"])),
                level_for_endpoint_assesement=row["LevelForEndPointAssesement"],
                is_local_authority=bool(int(row["IsLocalAuthority"])),
                qualification_category=qualification_category,
                qualification_type1=qualification_type1,
                is_deleted=bool(int(row["IsDeleted"])),
                created_date=self._parse_timestemp(row["CreatedDate"]),
                last_updated_date=self._parse_timestemp(row["LastUpdatedDate"]),
            )

    def _import_qualification_values(self):
        rows = self._clean_csv("qualification_values.csv")
        for row in rows:
            QualificationValue.objects.create(
                id=row["Id"],
                qualification_id=row["QualificationId"],
                funding_year_id=row["FundingYearId"],
                funding_value=row["FundingValue"],
                is_deleted=bool(int(row["IsDeleted"])),
                created_date=self._parse_timestemp(row["CreatedDate"]),
                last_updated_date=self._parse_timestemp(row["LastUpdatedDate"]),
            )

    @transaction.atomic
    def handle(self, **options):
        self.stdout.write("Importing init data...")

        QualificationValue.objects.all().delete()
        Qualification.objects.all().delete()
        FundingYear.objects.all().delete()
        AwardingBody.objects.all().delete()

        self._import_funding_years()
        self._import_awarding_bodies()
        self._import_qualifications()
        self._import_qualification_values()

        self.stdout.write("...Done")
