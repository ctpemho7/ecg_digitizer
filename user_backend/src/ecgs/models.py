import httpx
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from users.models import UserModel

from user_backend.settings import LABEL_STUDIO_TOKEN, LABEL_STUDIO_SYNC
from ecgs.utils import HashedUploadTo


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

    def get_buttons(self):
        buttons = []
        if self.status == self.CHOICES[0][0]:  # Создано - на разметку
            images = self.images.all()
            for i in range(len(images)):
                buttons.append({
                    'text': f'Разметить изображение {i+1}',
                    'href': f'http://localhost:8080/projects/1/data?tab=1&task={images[i].task_id}',
                })

        if self.status == self.CHOICES[3][0]:  # Размечено - оцифровать
            buttons.append({
                'text': f'Оцифровать ЭКГ',
                'href': reverse("ecgs:digitize_ecg",  args=[self.id]),
            })

        if self.status == self.CHOICES[4][0]:  # На оцифровке - ждать
            buttons.append({
                'text': f'На оцифровке',
                'href': '#',
                'args': 'disabled',
            })

        if self.status == self.CHOICES[5][0]:  # Оцифровано - оцифровать
            buttons.append({
                'text': f'Скачать',
                'href': reverse("ecgs:download_ecg",  args=[self.id]),
            })
        return buttons


class EcgImage(models.Model):
    ecg = models.ForeignKey(EcgModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=HashedUploadTo('images/'))
    task_id = models.IntegerField(null=True, blank=True)
    annotation_id = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=EcgModel, dispatch_uid="sync")
def sync_storage(sender, instance, **kwargs):
    url = LABEL_STUDIO_SYNC
    headers = {"Authorization": f"Token {LABEL_STUDIO_TOKEN}"}
    response = httpx.post(url, headers=headers)
    # print(response.json())
    print('Task synced successfully!')
