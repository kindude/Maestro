from django.contrib.auth import login
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user, backend=user.backend)

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
