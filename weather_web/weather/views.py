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


class PlaceDetailView(generic.DetailView, LoginRequiredMixin):
    template_name = "weather/place_detail.html"
    model = Place


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
        data = GetWeatherForecasts('Praha')
        print(data)
    except:
        pass

    return render(request, "weather/weather_test.html", )


class GetWeatherForecasts:
    """
    class for getting weather forecast from multiple sources
    """

    def __init__(self, place):
        self.weather_data = self.get_weather_data(place)

    def get_weather_data(self, place):
        '''
        collects weather data for given place from all sources and returns them in dictionary of lists
        :param place: str
        '''
        temperatures_openweather, dates_openweather = self.get_data_openweather(
            place)
        temperatures_in_pocasi, dates_in_pocasi = self.get_in_pocasi_data(
            place)
        temperatures_yr, dates_yr = self.get_yr_data(
            place)

        weather_data = self.prepare_weather_data(
            dates_openweather, temperatures_openweather, dates_in_pocasi, temperatures_in_pocasi, temperatures_yr, dates_yr)
        print(weather_data)
        weather_data = self.fill_in_vectors(
            weather_data, weather_data['length'])

        return weather_data

    def prepare_weather_data(self, dates_openweather, temperatures_openweather, dates_in_pocasi, temperatures_in_pocasi, temperatures_yr, dates_yr):
        '''
        prepares weather data from different sources into one dictionary weather_data, which it returns
        :param dates_openweather: list
        :param temperatures_openweather: list
        :param dates_in_pocasi: list
        :param temperatures_in_pocasi: list
        :param temperatures_yr: list
        :param dates_yr: list
        '''
        weather_data = {}

        max_length = max(len(dates_in_pocasi), len(
            dates_openweather), len(dates_yr))
        print(max_length)

        if max_length == len(dates_yr):
            weather_data['dates'] = dates_yr
        elif max_length == len(dates_in_pocasi):
            weather_data['dates'] = dates_in_pocasi
        else:
            weather_data['dates'] = dates_in_pocasi

        weather_data['temperatures_openweather'] = temperatures_openweather
        weather_data['temperatures_in_pocasi'] = temperatures_in_pocasi
        weather_data['temperatures_yr'] = temperatures_yr
        weather_data['length'] = max_length

        weather_data['dates_openweather'] = dates_openweather
        weather_data['dates_in_pocasi'] = dates_in_pocasi
        weather_data['dates_yr'] = dates_yr

        return weather_data

    def get_data_openweather(self, place):
        '''
        get weather forecast data from openweather api and returns temperatures and dates lists
        :param place: str
        '''

        token = '3826180b6619b9e8655cd67a2fa30f52'
        url = 'http://api.openweathermap.org/data/2.5/forecast'

        parameters = {
            'APIKEY': token,
            'q': place,
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

    def get_yr_data(self, place):
        '''
        get weather forecast data from yr weather api from selected place and returns temperatures and dates lists
        :param place: str
        '''
        ['Praha', 'Brno', 'Kvilda', 'Nová Paka']
        latslongs = {
            'Praha': {'lat': 50.5, 'long': 14.25},
            'Brno': {'lat': 49.20, 'long': 16.60},
            'Kvilda': {'lat': 49.02, 'long': 13.58},
            'Nová Paka': {'lat': 50.49, 'long': 15.52}
        }

        url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latslongs[place]['lat']}&lon={latslongs[place]['long']}"
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

    def get_in_pocasi_data(self, place):
        '''
        get weather forecast data for given place from in Počasí website and returns temperatures and dates lists
        :param place: str
        '''
        urls = {'Praha': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/praha/praha-324',
                'Kvilda': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/kvilda-4588/',
                'Brno': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/jihomoravsky/brno-25/',
                'Nová Paka': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/kralovehradecky/nova-paka-271/'}

        url = urls[place]
        api_request = requests.get(url)
        soup = BeautifulSoup(api_request.content, 'html.parser')

        temperatures, dates = [], []

        actual_temp = soup.find(class_='alfa mb-1')
        actual_temp = actual_temp.text
        actual_temp = re.findall("-* *\d*\d\.*\d*", actual_temp)
        temperatures.append(float(actual_temp[0]))
        dates.append(datetime.date.today().strftime('%d. %m.'))

        indexes = ['day'+str(i) for i in range(1, 8)]
        for i in range(len(indexes)):
            try:
                results = soup.find(id=indexes[i])
                results = results.find(class_="mt-1 strong")
                results = float(
                    (re.findall("-* *\d*\d\.*\d*", results.text))[0])
                temperatures.append(results)
                date = datetime.date.today() + datetime.timedelta(days=(i+1))
                dates.append(date.strftime('%d. %m.'))

            except AttributeError:
                print(f"{indexes[i]} index was not found")

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
