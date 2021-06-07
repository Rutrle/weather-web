from django.urls import path
from .views import TestBaseView, WeatherIndexView, PlaceListView

app_name = 'weather'

urlpatterns = [
    path('base/', TestBaseView.as_view(), name='base_test'),
    path('', WeatherIndexView.as_view(), name='weather_index'),
    path('places/', PlaceListView.as_view(), name='place_list')
]
