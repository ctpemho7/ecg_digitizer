from django.contrib import admin

from ecgs.models import EcgModel, EcgImage


class ImageAdmin(admin.TabularInline):
    model = EcgImage
    fields = ('id', 'image')


@admin.register(EcgModel)
class EcgModelAdmin(admin.ModelAdmin):
    list_display = ("status", "name", "description", "date", "path", "owner")
    inlines = (ImageAdmin, )
