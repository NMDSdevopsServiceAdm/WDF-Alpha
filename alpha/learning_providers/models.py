from django.db import models


class LearningProvider(models.Model):
    provider = models.CharField(max_length=255, blank=False)
