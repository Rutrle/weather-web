from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserPreference


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
        fields = ("username", "email")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        fields = ('degrees',)
        model = UserPreference
