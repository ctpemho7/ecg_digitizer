from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from rest_framework.decorators import api_view
from rest_framework.request import Request

from ecgs.clients.detection import DetectionClient
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


@api_view(["GET"])
def get_predict(request: Request, filename: str) -> JsonResponse:
    """
    Получить результат модели детекции отведений ЭКГ.

    :param Request request: Объект запроса
    :param filename: наименование фотографии ЭКГ с расширением
    :return:
    """

    result = DetectionClient().get_predict(filename)
    return JsonResponse(result, safe=False)
