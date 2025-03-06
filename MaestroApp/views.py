from django.shortcuts import render, redirect
from .decorators import student_required, teacher_required, admin_required
from .models import MaestroClass, testClass, MaestroInstrument
from django.contrib.auth.decorators import login_required
from .forms import CreateModelClass


def index(request):
    classes_objects = MaestroClass.objects.all()
    context = {'classes': classes_objects}
    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html')

@admin_required
def create_class(request):
    if request.method == "POST":
        form = CreateModelClass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('find_classes')

    else:
        form = CreateModelClass()

    return render(request, 'pages/create_class.html', {'form': form})


def find_classes(request):
    classes_objects = MaestroClass.objects.all()
    context = {'classes': classes_objects}

    return render(request, 'pages/find_classes.html', context)


@student_required
def play(request):
    return render(request, 'pages/play.html')


@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')
