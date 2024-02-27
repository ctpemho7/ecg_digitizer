from rest_framework import viewsets, mixins

from users.models import UserModel, PatientToDocktor
from users.serializers import UserModelSerializer, PatientToDocktorSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователем.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]


# реализация PatientToDocktor
class PatientToDocktorViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """
    ViewSet для работы с прикреплением к врачу.
    Обеспечивает методы `retrieve`, `create`, `destroy` для получения, создания и удаления связи.

    """
    queryset = PatientToDocktor.objects.all()
    serializer_class = PatientToDocktorSerializer

    def get_queryset(self):
        """
        Возвращает queryset из прикрепленных к врачу пациентов.
        """
        doctor_pk = self.kwargs['doctor_pk']
        return PatientToDocktor.objects.filter(doctor__id=doctor_pk)


class PatientToDocktorListViewSet(mixins.ListModelMixin,
                                  viewsets.GenericViewSet):
    """
    ViewSet для получения прикрепленных к врачу пользователей.
    """
    queryset = PatientToDocktor.objects.all()
    serializer_class = PatientToDocktorSerializer

    def get_queryset(self):
        """
        Возвращает queryset из прикрепленных к врачу пациентов.
        """
        doctor_pk = self.kwargs['doctor_pk']
        return PatientToDocktor.objects.filter(doctor__id=doctor_pk)
