from django.db import models

from users.models import UserModel


class EcgModel(models.Model):
    CHOICES = (
        ("Created", 'Создано'),
        ("Added", 'Добавлено фото'),
        ("Detection", 'ЭКГ на разметке'),
        ("Detected", 'ЭКГ размечена'),
        ("Digitizing", 'ЭКГ на оцифровке'),
        ("Digitized", 'ЭКГ оцифровано'),
    )

    status = models.CharField(max_length=10, choices=CHOICES)

    name = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    path = models.FileField(null=True, blank=True)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
