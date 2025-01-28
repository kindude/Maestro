
from django.urls import path

from MaestroApp.views import index, about

urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about')
]