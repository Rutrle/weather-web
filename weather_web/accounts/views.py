from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from . import forms
from django.views.generic import TemplateView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# Create your views here.


def sign_up_view(request):
    user_form = forms.UserCreateForm
    if request.method == 'POST':
        user_form = user_form(request.POST)

        if user_form.is_valid():
            user_form.save()
            user_preference_form = forms.UserPreferenceForm
            user_preference_form = user_preference_form(request.POST)
            preferences = user_preference_form.save(commit=False)
            preferences.user = request.user
            preferences.save()

            return redirect("login")

    context = {'form': user_form}
    return render(request, "accounts/signup.html", context)


def login_view(request):
    form = AuthenticationForm

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('weather:weather_index'))

        else:
            messages.error(request, "Invalid username or password.")
            # return render(request, 'accounts/login.html', {'form': form})

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:goodbye'))


class GoodbyeView(TemplateView):
    template_name = 'accounts/goodbye.html'
