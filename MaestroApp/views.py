from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .models import MaestroClass

from django.contrib.auth import logout


def index(request):
    classes = MaestroClass.objects.all()
    context = {'classes': classes}

    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html')


def play(request):
    return render(request, 'pages/play.html')


def dashboard(request):
    return render(request, 'pages/dashboard.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        else:
            messages.error(request, form.errors.as_data())
    else:
        form = RegisterForm()

    return render(request, 'pages/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('dashboard')
        else:
            messages.error(request, form.errors.as_data())
    else:
        form = LoginForm()

    return render(request, 'pages/login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
