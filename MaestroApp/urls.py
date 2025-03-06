
from django.urls import path

from MaestroApp.views import index, about, play, dashboard, create_class, find_classes
from MaestroApp.auth_views import *


urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard', dashboard, name='dashboard'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('create-class/', create_class, name='create_class'),
    path('find-classes/', find_classes, name='find_classes')
]