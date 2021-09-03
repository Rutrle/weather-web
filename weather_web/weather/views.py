from django.shortcuts import render
from django.views import generic
from .models import Place
from .forms import PlaceForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class TestBaseView(generic.TemplateView):
    template_name = 'weather/weather_base.html'


class WeatherIndexView(generic.TemplateView):
    template_name = 'weather/weather_index.html'


class PlaceCreateView(generic.CreateView, LoginRequiredMixin):
    #form_class = PlaceForm
    model = Place
    fields = ('name', 'longtitude', 'latitude')

    template_name = 'weather/place_create.html'

    def get_success_url(self):
        return reverse('weather:weather_index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(self.request.user)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class PlaceListView(generic.ListView):
    model = Place


class PlaceDetailView(generic.DetailView):
    template_name = "weather/place_detail.html"
    model = Place
