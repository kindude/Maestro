
from django.urls import path

from MaestroApp.views import index, about, play, dashboard_view
from . import views
from MaestroApp.views import test_dashboard



urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/test/', test_dashboard, name='test_dashboard'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]