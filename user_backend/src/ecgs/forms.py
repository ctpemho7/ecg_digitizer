from django import forms

from ecgs.models import EcgModel, EcgImage
from users.models import UserModel


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class EcgForm(forms.ModelForm):
    class Meta:
        model = EcgModel
        fields = ('name', 'description', 'amplitude', 'write_speed', 'date', 'algorithm', 'images')

    images = MultipleFileField(label='Изображения',)
