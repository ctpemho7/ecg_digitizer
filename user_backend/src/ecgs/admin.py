import io
import os
from zipfile import ZipFile

from django.contrib import admin
from django.http import HttpResponse

from ecgs.models import EcgModel, EcgImage
from ecgs.utils import get_from_s3


@admin.action(description="Скачать оцифрованные ЭКГ")
def download_ecg(modeladmin, request, queryset):
    byte_stream = io.BytesIO()
    zf = ZipFile(byte_stream, "w")
    zip_name = f'wfdb-collection.zip'

    for ecg in queryset:
        header = get_from_s3(ecg.header_path.name)
        signal = get_from_s3(ecg.signal_path.name)
        header = get_from_s3(header)
        signal = get_from_s3(signal)
        zf.write(signal, os.path.basename(signal))
        zf.write(header, os.path.basename(header))

    zf.close()

    response = HttpResponse(byte_stream.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename="%s"' % zip_name
    return response


class ImageAdmin(admin.TabularInline):
    model = EcgImage
    fields = ('id', 'image', 'task_id', 'annotation_id')
    readonly_fields = ['task_id', 'annotation_id']


@admin.register(EcgModel)
class EcgModelAdmin(admin.ModelAdmin):
    list_display = ("name", "status",  "description", "date", "algorithm")
    inlines = (ImageAdmin, )
    list_filter = ["date", "algorithm", "status", "owner"]
    actions = [download_ecg]
