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
        fields = ('name', 'description', 'amplitude', 'write_speed', 'date', 'images')

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите название',
    }))
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите описание',
    }))
    amplitude = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите скорость записи',
    }),
        max_value=100,
        min_value=0)
    write_speed = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите скорость записи',
    }),
        max_value=100,
        min_value=0)
    date = forms.DateField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите дату',
    }))

    images = MultipleFileField(label='Изображения', )
