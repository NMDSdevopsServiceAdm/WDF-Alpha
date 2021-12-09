from django.db import models


class WDFModel(models.Model):
    created_date = models.DateTimeField(null=True, blank=True)
    last_updated_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class AwardingBody(WDFModel):
    name = models.CharField(max_length=100, blank=False)

    @property
    def name_human(self):
        if self.name == "AO-Unknown":
            return ""
        return self.name.split("-", 1)[1]


class FundingYear(WDFModel):
    year_code = models.CharField(max_length=7, blank=False)
    description = models.CharField(max_length=7, blank=False)


class Qualification(WDFModel):
    qualification_code = models.CharField(max_length=20, blank=False)
    qualification_title = models.CharField(max_length=200, blank=False)
    qualification_type2 = models.CharField(max_length=100, blank=False)
    awarding_body = models.ForeignKey(AwardingBody, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(null=True, blank=True, default=None)
    num_credits = models.PositiveIntegerField(default=0)
    is_part_of_apprenticeship = models.BooleanField(default=False)
    is_pre_funded = models.BooleanField(default=False)
    is_endpoint_assesement = models.BooleanField(default=False)
    level_for_endpoint_assesement = models.PositiveIntegerField(
        null=True, blank=True, default=None
    )
    is_local_authority = models.BooleanField(default=False)

    # new fields we've added
    # Apprenticeship / Qualification / Learning Programme
    qualification_category = models.CharField(max_length=100, blank=False)
    # Award / Certificate / Diploma
    qualification_type1 = models.CharField(max_length=100, blank=True)


class QualificationValue(WDFModel):
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    funding_year = models.ForeignKey(FundingYear, on_delete=models.CASCADE)
    funding_value = models.PositiveIntegerField(default=0)

    @property
    def funding_value_human(self):
        return f"£{self.funding_value:,}"
