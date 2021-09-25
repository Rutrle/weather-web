from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from .models import Place
from .forms import PlaceForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
import requests
import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
import re


class TestBaseView(generic.TemplateView):
    template_name = 'weather/weather_base.html'


class WeatherIndexView(generic.TemplateView):
    template_name = 'weather/weather_index.html'


class AboutView(generic.TemplateView):
    template_name = 'weather/about.html'


class PlaceCreateView(generic.CreateView, LoginRequiredMixin):
    form_class = PlaceForm

    template_name = 'weather/place_create.html'

    def get_success_url(self):
        return reverse('weather:place_detail', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(self.request.user)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class PlaceListView(generic.ListView):
    model = Place


@login_required
def place_detail_view(request, pk):
    place = get_object_or_404(Place, pk=pk)
    weather_data = GetWeatherForecasts(place.longtitude, place.latitude)
    print(weather_data.weather_data)
    context = {'place': place,
               'dates': weather_data.weather_data['dates'],
               'temperatures_yr': weather_data.weather_data['temperatures_yr'],
               'temperatures_openweather': weather_data.weather_data['temperatures_openweather']
               }

    return render(request, "weather/place_detail.html", context)


@login_required
def place_delete_view(request, pk):
    place = get_object_or_404(Place, pk=pk)
    if request.method == "POST":
        if place.author == request.user:
            place.delete()
            return redirect(reverse('weather:place_list'))
        else:
            raise PermissionDenied

    return render(request, "weather/place_delete.html", )


@login_required
def place_update_view(request, pk):
    place = get_object_or_404(Place, pk=pk)
    form = PlaceForm(request.POST or None, instance=place)

    context = {
        'form': form
    }

    if request.method == "POST":
        if place.author == request.user:
            if form.is_valid():
                form.save()
            return redirect(reverse('weather:place_list'))
        else:
            raise PermissionDenied

    return render(request, "weather/place_create.html", context)


class PlaceUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = Place
    fields = ('name', 'longtitude', 'latitude')

    template_name = 'weather/place_create.html'

    def get_success_url(self):
        return reverse('weather:place_list')


def weather_forecast_test_view(request):
    print('praha')
    try:
        weather_forecast = GetWeatherForecasts('Praha')
        weather_data = weather_forecast.weather_data
        print(weather_data)
    except:
        pass

    return render(request, "weather/weather_test.html", )


class GetWeatherForecasts:
    """
    class for getting weather forecast from multiple sources
    """

    def __init__(self, longtitude, latitude):
        self.weather_data = self.get_weather_data(longtitude, latitude)

    def get_weather_data(self, longtitude, latitude):
        '''
        collects weather data for given place from all sources and returns them in dictionary of lists
        :param place: str
        '''
        temperatures_openweather, dates_openweather = self.get_data_openweather(
            longtitude, latitude)
        temperatures_yr, dates_yr = self.get_yr_data(
            longtitude, latitude)

        weather_data = self.prepare_weather_data(
            dates_openweather, temperatures_openweather, temperatures_yr, dates_yr)
        # print(weather_data)
        weather_data = self.fill_in_vectors(
            weather_data, weather_data['length'])

        return weather_data

    def prepare_weather_data(self, dates_openweather, temperatures_openweather, temperatures_yr, dates_yr):
        '''
        prepares weather data from different sources into one dictionary weather_data, which it returns
        :param dates_openweather: list
        :param temperatures_openweather: list
        :param temperatures_yr: list
        :param dates_yr: list
        '''
        weather_data = {}

        max_length = max(len(
            dates_openweather), len(dates_yr))
        print(max_length)

        if max_length == len(dates_yr):
            weather_data['dates'] = dates_yr
        else:
            weather_data['dates'] = dates_openweather

        weather_data['temperatures_openweather'] = temperatures_openweather
        weather_data['temperatures_yr'] = temperatures_yr
        weather_data['length'] = max_length

        weather_data['dates_openweather'] = dates_openweather
        weather_data['dates_yr'] = dates_yr

        return weather_data

    def get_data_openweather(self, longtitude, latitude):
        '''
        get weather forecast data from openweather api and returns temperatures and dates lists
        :param place: str
        '''

        api_key = '3826180b6619b9e8655cd67a2fa30f52'
        url = f' http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longtitude}&appid={api_key}'

        parameters = {
            'units': 'metric'
        }

        api_request = requests.get(url, params=parameters)
        api_request = api_request.json()

        dates, temperatures = [], []
        for item in api_request['list']:
            date = item['dt']
            temperature = item['main']['temp']

            date = datetime.datetime.fromtimestamp(date)

            dates.append(date)
            temperatures.append(temperature)

        temperatures, dates = self.prepare_api_data(
            temperatures, dates)

        return temperatures, dates

    def prepare_api_data(self, temperatures, dates):
        '''
        clears and prepares data from  api which has multiple temperatures per single day
        :param temperatures: list
        :param dates: list
        '''
        max_day_temperatures, prepared_dates = [], []

        sorted_temperatures = defaultdict(list)

        for i in range(len(dates)):
            if(dates[i] >= datetime.datetime.today()):
                sorted_temperatures[dates[i].strftime(
                    '%d. %m.')].append(temperatures[i])

        for date in sorted_temperatures:
            max_day_temperatures.append((max(sorted_temperatures[date])))
            prepared_dates.append(date)

        today_date = (datetime.date.today())
        if prepared_dates[0] != today_date.strftime('%d. %m.'):
            prepared_dates.insert(0,  today_date.strftime('%d. %m.'))
            max_day_temperatures.insert(0, 'NA')

        return max_day_temperatures, prepared_dates

    def get_yr_data(self, longtitude, latitude):
        '''
        get weather forecast data from yr weather api from selected place and returns temperatures and dates lists
        :param place: str
        '''

        url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longtitude}"
        header = {
            "Accept": 'application/json',
            'User-Agent': 'weather app tryout https://github.com/Rutrle/Weather-app'
        }

        api_request = requests.get(url, headers=header)
        api_request = api_request.json()
        relevant_data = api_request['properties']['timeseries']

        temperatures, dates = [], []
        for weather_log in relevant_data:

            date = datetime.datetime.strptime(
                weather_log['time'], '%Y-%m-%dT%H:%M:%SZ')

            dates.append(date)
            temperatures.append(
                weather_log['data']['instant']['details']['air_temperature'])

        temperatures, dates = self.prepare_api_data(temperatures, dates)

        return temperatures, dates

    def fill_in_vectors(self, weather_data, length):
        '''
        uses fill_in_vector method to fill in lists in weather_data to length
        :param weather_data: dict
        '''
        for key in weather_data:
            if isinstance(weather_data[key], list):
                while len(weather_data[key]) < length:
                    weather_data[key].append('NA')

        return weather_data
