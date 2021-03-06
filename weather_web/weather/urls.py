from django.urls import path
from .views import TestBaseView, WeatherIndexView, PlaceListView, PlaceCreateView, place_detail_view, place_update_view, AboutView, place_delete_view, my_place_list_view

app_name = 'weather'

urlpatterns = [
    path('base/', TestBaseView.as_view(), name='base_test'),
    path('', WeatherIndexView.as_view(), name='weather_index'),
    path('about/', AboutView.as_view(), name='about'),
    path('places/', PlaceListView.as_view(), name='place_list'),
    path('places/create', PlaceCreateView.as_view(), name='place_create'),
    path('places/<int:pk>/detail', place_detail_view, name='place_detail'),
    path('places/<int:pk>/remove',
         place_delete_view, name='place_remove'),
    path('places/<int:pk>/edit', place_update_view, name='place_edit'),
    path('places/my', my_place_list_view, name='my_place_list')
]
