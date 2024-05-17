from django.urls import path

from ecgs.views import EcgListView, EcgCreateView, task_created, task_annotated

app_name = 'ecgs'

urlpatterns = [
    path('', EcgListView.as_view(), name='index'),
    path('create/', EcgCreateView.as_view(), name='ecg_create'),
    path('webhook/task_created', task_created, name='task_created'),
    path('webhook/task_annotated', task_annotated, name='task_annotated'),
]
