
from django.urls import path
from .views import index, about, play, test_dashboard, logout_view, dashboard,  create_class, find_classes
from MaestroApp.auth_views import *


urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard', dashboard, name='dashboard'),
    path('dashboard/test/', test_dashboard, name='test_dashboard'),
    path('logout/', logout_view, name='logout'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('create-class/', create_class, name='create_class'),
    path('find-classes/', find_classes, name='find_classes')
]