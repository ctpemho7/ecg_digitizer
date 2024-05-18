from django.urls import path

from ecgs.views import EcgListView, EcgCreateView, task_created, task_annotated, digitize_ecg

app_name = 'ecgs'

urlpatterns = [
    path('', EcgListView.as_view(), name='index'),
    path('create/', EcgCreateView.as_view(), name='ecg_create'),
    path('webhook/task_created', task_created, name='task_created'),
    path('webhook/task_annotated', task_annotated, name='task_annotated'),
    path('webhook/digitize_ecg/<int:ecg_id>', digitize_ecg, name='digitize_ecg'),
]
