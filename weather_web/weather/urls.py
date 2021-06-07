from django.urls import path
from .views import TestBaseView, WeatherIndex

app_name = 'weather'

urlpatterns = [
    path('base/', TestBaseView.as_view(), name='base_test'),
    path('', WeatherIndex.as_view(), name='weather_index')
]
