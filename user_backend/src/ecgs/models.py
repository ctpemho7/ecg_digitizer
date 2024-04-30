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
    amplitude = models.IntegerField()
    write_speed = models.IntegerField()
    header_path = models.FileField(upload_to="digitized", null=True, blank=True)
    signal_path = models.FileField(upload_to="digitized", null=True, blank=True)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    algorithm = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} от {self.date} {self.owner.last_name}"

    class Meta:
        verbose_name = 'ЭКГ'
        verbose_name_plural = 'ЭКГ'


class EcgImage(models.Model):
    ecg = models.ForeignKey(EcgModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")