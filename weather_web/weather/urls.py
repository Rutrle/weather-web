from django.urls import path
from .views import TestBaseView

app_name = 'weather'

urlpatterns = [
    path('base/', TestBaseView.as_view(), name='base_test'),
]
