from django.http import JsonResponse
from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request

from ecgs.clients.detection import DetectionClient
from ecgs.models import EcgModel


class EcgListView(ListView):
    model = EcgModel
    template_name = 'ecgs/ecgs.html'
    paginate_by = 3


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
