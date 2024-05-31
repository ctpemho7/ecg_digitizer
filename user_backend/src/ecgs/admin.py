import io
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
        mock_signal = 'digitized/00001_lr.dat'
        mock_header = 'digitized/00001_lr.hea'
        header = get_from_s3(mock_header)
        signal = get_from_s3(mock_signal)
        zf.write(signal, f'{ecg.name}.dat')
        zf.write(header, f'{ecg.name}.hea')

    zf.close()

    response = HttpResponse(byte_stream.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename="%s"' % zip_name
    return response


class ImageAdmin(admin.TabularInline):
    model = EcgImage
    fields = ('id', 'image')


@admin.register(EcgModel)
class EcgModelAdmin(admin.ModelAdmin):
    list_display = ("name", "status",  "description", "date", "algorithm")
    inlines = (ImageAdmin, )
    list_filter = ["date", "algorithm", "status", ]
    actions = [download_ecg]
