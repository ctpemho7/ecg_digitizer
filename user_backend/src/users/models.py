from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    CHOICES = (
        ("P", "Пациент"),
        ("D", "Врач"),
        ("DE", "Data Engineer"),
    )

    status = models.CharField(max_length=2, choices=CHOICES)
    REQUIRED_FIELDS = ["status"]


class PatientToDocktor(models.Model):
    doctor = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="doctor")
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="patient")

