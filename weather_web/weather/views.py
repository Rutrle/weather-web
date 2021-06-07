from django.shortcuts import render
from django.views import generic
from .models import Place


class TestBaseView(generic.TemplateView):
    template_name = 'weather/weather_base.html'


class WeatherIndexView(generic.TemplateView):
    template_name = 'weather/weather_index.html'


class PlaceListView(generic.ListView):
    model = Place
