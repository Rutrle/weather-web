from django.shortcuts import render
from django.views import generic


class TestBaseView(generic.TemplateView):
    template_name = 'weather_base.html'


class WeatherIndex(generic.TemplateView):
    template_name = 'weather_index.html'
