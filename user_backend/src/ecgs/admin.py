from django.contrib import admin

from ecgs.models import EcgModel

@admin.register(EcgModel)
class EcgModelAdmin(admin.ModelAdmin):
    list_display = ("status", "name", "description", "date", "path", "owner")
