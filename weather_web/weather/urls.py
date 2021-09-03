from django.urls import path
from .views import TestBaseView, WeatherIndexView, PlaceListView, PlaceCreateView

app_name = 'weather'

urlpatterns = [
    path('base/', TestBaseView.as_view(), name='base_test'),
    path('', WeatherIndexView.as_view(), name='weather_index'),
    path('places/', PlaceListView.as_view(), name='place_list'),
    path('places/create', PlaceCreateView.as_view(), name='place_create')
]
