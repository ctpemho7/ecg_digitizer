import io
import json
from zipfile import ZipFile

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from ecgs.forms import EcgForm
from ecgs.models import EcgModel, EcgImage
from ecgs.tasks import digitize_task
from ecgs.utils import get_from_s3, deskew_image
from users.models import UserModel


class EcgListView(ListView):
    model = EcgModel
    template_name = 'ecgs/ecgs.html'
    paginate_by = 50
    ordering = ['-id']


class EcgCreateView(CreateView):
    model = EcgModel
    form_class = EcgForm
    template_name = 'ecgs/ecg-create.html'
    success_url = reverse_lazy('ecgs:index')

    def form_valid(self, form):
        ecg_instance = form.instance
        ecg_instance.owner = UserModel.objects.get(id=1)
        ecg_instance.algorithm = "Fortune"
        ecg_instance.status = EcgModel.CHOICES[0][0]
        ecg_instance.save()
        # print(self.request)
        # print(self.request.FILES)
        for image in self.request.FILES.getlist('images'):
            # deskew image
            rotated = deskew_image(image)
            EcgImage.objects.create(ecg=ecg_instance, image=rotated)
        return super().form_valid(form)


@csrf_exempt
def task_created(request) -> JsonResponse:
    body = json.loads(request.body)
    for task in body['tasks']:
        # путь до изображения
        splitted = task['data']['image'].split('/')
        image_path = splitted[-2] + '/' + splitted[-1]
        # таска
        task_id = task['id']
        # присвоить номер таски
        ecg_image = EcgImage.objects.get(image=image_path)
        ecg_image.task_id = task_id
        ecg_image.save()
        print(f'for image with path {image_path} saved task_id {task_id}')

    return JsonResponse({}, status=201)


@csrf_exempt
def task_annotated(request) -> JsonResponse:
    body = json.loads(request.body)
    # путь до изображения
    splitted = body['task']['data']['image'].split('/')
    image_path = splitted[-2] + '/' + splitted[-1]
    # аннотация
    annotation_id = body['annotation']['id']
    print('image_path', image_path)
    ecg_image = EcgImage.objects.filter(image=image_path)[0]
    # присвоить номер аннотации
    ecg_image.annotation_id = annotation_id
    ecg_image.save()
    print(f'for image with path {image_path} saved annotation {annotation_id}')

    # дополнительно: если все изображения проаннотированы, то ЭКГ размечена
    # проверить, проставлены ли у всех изображений аннотации
    ecg_images = EcgImage.objects.filter(ecg=ecg_image.ecg)
    change_status = True
    for ecg_image in ecg_images:
        if ecg_image.annotation_id is None:
            change_status = False

    print('change_status', change_status)
    # если да, то сменить статус
    if change_status:
        ecg_image.ecg.status = EcgModel.CHOICES[3][0]
        ecg_image.ecg.save()
    return JsonResponse({}, status=201)


def digitize_ecg(request, ecg_id):
    digitize_task.delay(ecg_id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def download_ecg(request, ecg_id):
    ecg = EcgModel.objects.get(id=ecg_id)
    # header = get_from_s3(ecg.header_path.name)
    # signal = get_from_s3(ecg.signal_path.name)
    mock_signal = 'digitized/00001_lr.dat'
    mock_header = 'digitized/00001_lr.hea'
    header = get_from_s3(mock_header)
    signal = get_from_s3(mock_signal)

    byte_stream = io.BytesIO()
    zf = ZipFile(byte_stream, "w")

    zip_name = f'wfdb-{ecg_id}.zip'

    # zf.write(header, header.split('/')[-1])
    # zf.write(signal, signal.split('/')[-1])
    zf.write(signal, f'{ecg.name}.dat')
    zf.write(header, f'{ecg.name}.hea')
    zf.close()

    response = HttpResponse(byte_stream.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename="%s"' % zip_name
    return response
