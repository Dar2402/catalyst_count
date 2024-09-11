from django.db import models
from django.utils import timezone

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    domain = models.URLField( null=True, blank=True)
    year_founded = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    size_range = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    current_employee_estimate = models.CharField(max_length=255, null=True, blank=True)
    total_employee_estimate = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name