from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from .models import Place
from .forms import PlaceForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


class TestBaseView(generic.TemplateView):
    template_name = 'weather/weather_base.html'


class WeatherIndexView(generic.TemplateView):
    template_name = 'weather/weather_index.html'


class AboutView(generic.TemplateView):
    template_name = 'weather/about.html'


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


class PlaceUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = Place
    fields = ('name', 'longtitude', 'latitude')

    template_name = 'weather/place_create.html'

    def get_success_url(self):
        return reverse('weather:place_list')
