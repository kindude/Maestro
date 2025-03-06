from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Sum
from .models import MaestroRole, MaestroClass, MaestroAssignment

User = get_user_model()

def index(request):
    return render(request, 'pages/home.html', {"classes": MaestroClass.objects.all()})

def about(request):
    return render(request, 'pages/about.html')

def play(request):
    return render(request, 'pages/play.html')

@login_required
def dashboard_view(request):
    user = request.user

    context = {
        "role": user.role.role if user.role else "guest",  # Get user role
        "first_name": user.first_name,
        "middle_name": getattr(user, "middle_name", ""),  # If middle name exists
        "last_name": user.last_name,
        "email": user.email,
        "classes": user.classes.all() if user.is_teacher() or user.is_student() else [],
        "students": User.objects.filter(classes__in=user.classes.all(), role__role='student').distinct() if user.is_teacher() else [],
        "assignments": user.assignments.all() if user.is_student() else [],
        "total_students": User.objects.filter(role__role='student').count() if user.is_admin() else None,
        "total_teachers": User.objects.filter(role__role='teacher').count() if user.is_admin() else None,
    }

    return render(request, "dashboard/dashboard.html", context)

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = MaestroRole.objects.get_or_create(role='student')[0]
            user.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = UserCreationForm()

    return render(request, 'pages/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect('dashboard')
            messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'pages/login.html', {'form': form})


def test_dashboard(request):
    fake_user = {
        "role": "teacher",  # Change to "admin", "student", or "teacher" to test different views
        "first_name": "John",
        "middle_name": "Michael",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "classes": ["Class A", "Class B", "Class C"],  # Only for teachers and students
        "assignments": ["Assignment 1", "Assignment 2"],  # Only for students
        "students": ["Student X", "Student Y", "Student Z"],  # Only for teachers
        "total_students": 50,  # Only for admins
        "total_teachers": 10,  # Only for admins
    }
    return render(request, "pages/dashboard.html", fake_user)  # Updated path
