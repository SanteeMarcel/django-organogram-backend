from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=512)


class User(AbstractUser):
    reports_to = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reports",
    )
    company = models.ForeignKey(
        Company,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="employees",
    )
