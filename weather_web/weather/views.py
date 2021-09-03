from django.shortcuts import render
from django.views import generic
from .models import Place
from .forms import PlaceForm
from django.urls import reverse


class TestBaseView(generic.TemplateView):
    template_name = 'weather/weather_base.html'


class WeatherIndexView(generic.TemplateView):
    template_name = 'weather/weather_index.html'


class PlaceCreateView(generic.CreateView):
    form_class = PlaceForm
    template_name = 'weather/place_create.html'

    def get_success_url(self):
        return reverse('weather:weather_index')


class PlaceListView(generic.ListView):
    model = Place
