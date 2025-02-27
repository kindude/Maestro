
from django.urls import path

from MaestroApp.views import index, about, play, dashboard


urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard', dashboard, name='dashboard')
]