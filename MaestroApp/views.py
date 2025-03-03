from django.shortcuts import render
from MaestroApp.forms import createClassForm
from .decorators import student_required
from .models import MaestroClass, testClass
from django.contrib.auth.decorators import login_required
from .forms import createModelClass


def index(request):
    classes = MaestroClass.objects.all()
    context = {'classes': classes}

    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html')

def classes (request):
    context ={}
    form = createModelClass(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['form']= form
    return render(request, 'pages/classes.html', context)

def find_classes(request):
    classes = testClass.objects.all()
    context = {'classes': classes}

    return render(request, 'pages/Find_Classes.html', context)

@student_required
def play(request):
    return render(request, 'pages/play.html')

@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')
