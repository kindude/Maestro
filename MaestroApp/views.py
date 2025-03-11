from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import student_required, teacher_required, admin_required, is_admin
from .models import MaestroClass, testClass, MaestroInstrument, MaestroLesson, Assignment
from django.contrib.auth.decorators import login_required
from .forms import CreateModelClass, UpdateUserForm, CreateUpdateLessonForm, AssignmentForm
from django.http import JsonResponse



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


@login_required
def class_edit(request, class_id=None):
    if class_id:
        maestro_class = get_object_or_404(MaestroClass, id=class_id)
        if not (is_admin(request.user) or request.user in maestro_class.teachers.all()):
            return redirect("find_classes")
    else:
        if not is_admin(request.user):
            return redirect("find_classes")

        maestro_class = None

    if request.method == "POST":
        form = CreateModelClass(request.POST, instance=maestro_class)
        if form.is_valid():
            maestro_class = form.save(commit=False)
            maestro_class.save()
            form.save_m2m()
            maestro_class.teachers.set(form.cleaned_data["teacher"])
            return redirect("find_classes")
    else:
        form = CreateModelClass(instance=maestro_class)

    return render(request, "pages/create_class.html", {"form": form, "maestro_class": maestro_class})


@login_required
def lesson_create_edit(request, class_id, lesson_id=None):
    if lesson_id:
        maestro_lesson = get_object_or_404(MaestroLesson, id=lesson_id)
        if not (is_admin(request.user) or request.user in maestro_lesson.associated_class.teachers.all()):
            return redirect("find_classes")
    else:
        if not is_admin(request.user):
            return redirect("find_classes")

        maestro_lesson = None

    if request.method == "POST":
        form = CreateUpdateLessonForm(request.POST, instance=maestro_lesson)
        if form.is_valid():
            maestro_lesson = form.save(commit=False)
            maestro_lesson.save()
            return redirect("find_classes")
    else:
        form = CreateUpdateLessonForm(instance=maestro_lesson)

    return render(request, "pages/create_edit_lesson.html", {"form": form, "maestro_lesson": maestro_lesson})

# Test view (optional, can be removed)
def test_view(request):
    return render(request, 'pages/login.html')

@login_required
def test_dashboard(request):
    user = request.user
    context = request.user
    return render(request, 'pages/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def find_classes(request):
    search_query = request.GET.get("search", "").strip()

    if search_query:
        classes = MaestroClass.objects.filter(title__icontains=search_query)
    else:
        classes = MaestroClass.objects.all()

    return render(request, "pages/find_classes.html", {"classes": classes, "search_query": search_query})


@login_required
def update_user_profile(request):
    user = request.user

    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = UpdateUserForm(instance=user)

    return render(request, "pages/update_profile.html", {"form": form})


@login_required
def notifications(request):
    return render(request, 'pages/notifications.html')

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({"success": True})

def assignment_detail_view(request, class_id, lesson_id, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, lesson__id=lesson_id, lesson__associated_class__id=class_id)
    return render(request, 'assignments/detail.html', {'assignment': assignment})

def is_admin_or_teacher(user):
    return user.is_staff or user.groups.filter(name='Teacher').exists()

@login_required
def assignments_list_view(request):  # <- Make sure the name is correct
    assignments = Assignment.objects.all()

    # Handle form submission (adding a new assignment)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignments_list')
    else:
        form = AssignmentForm()

    return render(request, 'assignments/list.html', {
        'assignments': assignments,
        'form': form,
        'is_admin_or_teacher': is_admin_or_teacher(request.user)
    })