
from django.urls import path
from .views import index, about, play, dashboard, test_dashboard, login_view, register_view, logout_view




urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard', dashboard, name='dashboard'),
    path('dashboard/test/', test_dashboard, name='test_dashboard'),
    path('logout/', logout_view, name='logout'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
