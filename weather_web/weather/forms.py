from django import forms
from .models import Place


class PlaceForm(forms.ModelForm):
    class Meta():
        model = Place
        fields = ('name', 'author', 'longtitude', 'latitude')


''' 
class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"
'''
