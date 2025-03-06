from django.contrib.auth import logout
from django.shortcuts import render, redirect

from .decorators import student_required, teacher_required, admin_required
from .models import MaestroClass, testClass, MaestroInstrument
from django.contrib.auth.decorators import login_required
from .forms import CreateModelClass



def index(request):
    classes_objects = MaestroClass.objects.all()
    context = {'classes': classes_objects}
    return render(request, 'pages/home.html', context)

@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')

def about(request):
    return render(request, 'pages/about.html')

def about(request):
    return render(request, 'pages/about.html')


def play(request):
    return render(request, 'pages/play.html')

@admin_required
def create_class(request):
    if request.method == "POST":
        form = CreateModelClass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('find_classes')

    else:
        form = CreateModelClass()

# Test view (optional, can be removed)
def test_view(request):
    return render(request, 'pages/login.html')

def test_dashboard(request):
    return render(request, 'pages/dashboard.html')

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirects to the login page


def find_classes(request):
    classes_objects = MaestroClass.objects.all()
    context = {'classes': classes_objects}

    return render(request, 'pages/find_classes.html', context)
