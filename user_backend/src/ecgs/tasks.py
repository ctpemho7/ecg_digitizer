import httpx
from celery import shared_task

from ecgs.schemas import EcgParams
from ecgs.models import EcgModel


@shared_task
def digitize_task(ecg_id):
    print('digitizing for', ecg_id)

    ecg = EcgModel.objects.get(id=ecg_id)
    ecg.status = EcgModel.CHOICES[4][0]
    ecg.save()
    url = 'http://host.docker.internal:8010/digitize'
    body = EcgParams(
        images={
            str(image.image): str(image.annotation_id)
            for image in ecg.images.all()
        },
        amplitude=ecg.amplitude,
        write_speed=ecg.write_speed,
    )

    response = httpx.post(url, json=body.dict(), timeout=15.0)
    response_data = response.json()
    print(response_data)
    if response_data:
        ecg.status = EcgModel.CHOICES[5][0]
        ecg.save()
