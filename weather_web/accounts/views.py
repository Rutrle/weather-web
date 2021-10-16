from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import UserPreference
from . import forms
from django.views.generic import TemplateView
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages


def sign_up_view(request):
    user_form = forms.UserCreateForm
    if request.method == 'POST':
        user_form = user_form(request.POST)

        if user_form.is_valid():
            user_form.save()
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

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_preference_update_view(request):
    user = request.user
    preference = get_object_or_404(UserPreference, user=user)
    user_form = forms.UserUpdateForm(instance=user)
    preference_form = forms.UserPreferenceForm(instance=preference)

    if request.method == 'POST':
        preference_form = forms.UserPreferenceForm(
            request.POST, instance=preference)
        user_form = forms.UserUpdateForm(request.POST, instance=user)
        if preference_form.is_valid():
            preference_form.save()

        if user_form.is_valid():
            user_form.save()

    print(user.username)
    print(preference.user.username)
    print(preference.places.all())

    for item in preference.places.all():
        print(item)

    context = {'form': user_form,
               'form2': preference_form
               }
    return render(request, 'accounts/edit.html', context)


@login_required
def password_change(request):
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        password_form = PasswordChangeForm(
            user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            return redirect(reverse("accounts:login"))

    context = {
        'form': password_form
    }
    return render(request, 'accounts/edit_password.html', context)


@ login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:goodbye'))


class GoodbyeView(TemplateView):
    template_name = 'accounts/goodbye.html'
