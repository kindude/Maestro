
from django.urls import path

from MaestroApp.views import index, about, play, dashboard
from . import views



urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard', dashboard, name='dashboard'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]