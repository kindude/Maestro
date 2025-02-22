
from django.urls import path

from MaestroApp.views import index, about, play

urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play')
]