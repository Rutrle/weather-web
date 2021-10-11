from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserPreference
from weather.models import Place


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ('degrees', 'places')
        labels = {
            'degrees': 'Degrees units'
        }

    places = forms.ModelMultipleChoiceField(
        queryset=Place.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='My favorite places'
    )
