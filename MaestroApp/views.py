from django.shortcuts import render

from .decorators import student_required
from .models import MaestroClass
from django.contrib.auth.decorators import login_required


def index(request):
    classes = MaestroClass.objects.all()
    context = {'classes': classes}

    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html')


@student_required
def play(request):
    return render(request, 'pages/play.html')

@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')
