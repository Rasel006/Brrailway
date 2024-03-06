from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from train.models import Train
# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trains = Train.objects.all()
        context['trains'] = trains
        return context
class AboutView(TemplateView):
    template_name = 'about.html'
class TrainView(TemplateView):
    template_name = 'trains.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trains = Train.objects.all()
        context['trains'] = trains
        return context
    
