from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=255, blank=False)
    workplace = models.CharField(max_length=255, blank=False)
    job_role = models.CharField(max_length=255, blank=False)
