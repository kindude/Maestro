from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Existing views
def index(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def play(request):
    return render(request, 'pages/play.html')

def dashboard(request):
    return render(request, 'pages/dashboard.html')

# Register view
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  
    else:
        form = UserCreationForm()
    
    return render(request, 'pages/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'pages/login.html', {'form': form})

# Test view (optional, can be removed)
def test_view(request):
    return render(request, 'pages/login.html')

def test_dashboard(request):
    return render(request, 'pages/dashboard.html')

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirects to the login page