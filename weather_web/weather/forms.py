from django import forms
from .models import Place


class PlaceForm(forms.ModelForm):
    class Meta():
        model = Place
        fields = ('name', 'longtitude', 'latitude')
        help_texts = {
            'longtitude': 'Signed degrees format, values between -180 and 180',
            'latitude': 'Signed degrees format,  values between -90 and 90',
        }

