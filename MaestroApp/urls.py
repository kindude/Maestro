
from django.urls import path

from MaestroApp.views import index, about, play, dashboard, classes, find_classes
from MaestroApp.auth_views import *


urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard', dashboard, name='dashboard'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('classes/', classes, name = 'classes'),
    path('findclasses/', find_classes, name = 'findclasses')
]