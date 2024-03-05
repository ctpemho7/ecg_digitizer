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

    def __str__(self):
        return f"{self.name} от {self.date} {self.owner.last_name}"

    class Meta:
        verbose_name = 'ЭКГ'
        verbose_name_plural = 'ЭКГ'


class EcgImage(models.Model):
    ecg = models.ForeignKey(EcgModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField()