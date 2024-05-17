import json

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from ecgs.forms import EcgForm
from ecgs.models import EcgModel, EcgImage
from users.models import UserModel


class EcgListView(ListView):
    model = EcgModel
    template_name = 'ecgs/ecgs.html'
    paginate_by = 10


class EcgCreateView(CreateView):
    model = EcgModel
    form_class = EcgForm
    template_name = 'ecgs/ecg-create.html'
    success_url = reverse_lazy('ecgs:index')

    def form_valid(self, form):
        ecg_instance = form.instance
        ecg_instance.owner = UserModel.objects.get(id=1)
        ecg_instance.algorithm = "Fortune"
        ecg_instance.save()
        print(self.request)
        print(self.request.FILES)
        for image in self.request.FILES.getlist('images'):
            EcgImage.objects.create(ecg=ecg_instance, image=image)
        return super().form_valid(form)


@csrf_exempt
def task_created(request) -> JsonResponse:
    body = json.loads(request.body)
    # путь до изображения
    splitted = body['task']['data']['image'].split('/')
    image_path = splitted[-2] + '/' + splitted[-1]
    # таска
    task_id = body['task']['id']
    # присвоить номер таски
    ecg_image = EcgImage.objects.get(image=image_path)
    ecg_image.task_id = task_id
    ecg_image.save()
    return JsonResponse({}, status=201)


@csrf_exempt
def task_annotated(request) -> JsonResponse:
    body = json.loads(request.body)
    # путь до изображения
    splitted = body['task']['data']['image'].split('/')
    image_path = splitted[-2] + '/' + splitted[-1]
    # аннотация
    annotation_id = body['annotation']['id']
    ecg_image = EcgImage.objects.get(image=image_path)
    # присвоить номер аннотации
    ecg_image.annotation_id = annotation_id
    ecg_image.save()
    print(ecg_image)
    print(ecg_image.annotation_id)
    return JsonResponse({}, status=201)