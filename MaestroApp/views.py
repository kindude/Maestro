from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import student_required, teacher_required, admin_required, is_admin, is_teacher
from .models import MaestroClass, MaestroLesson, MaestroAssignment, MaestroUser, MaestroNotification, \
    UserNotificationStatus
from django.contrib.auth.decorators import login_required
from .forms import CreateModelClass, UpdateUserForm, CreateUpdateLessonForm, CreateUpdateAssignmentForm, \
    EnrollStudentsForm
from django.utils.text import slugify
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .utils import create_notification
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

@login_required
def play(request):
    key_note_map = {
        # Lower octave (C3–B3)
        'z': 'C3', 's': 'C#3', 'x': 'D3', 'd': 'D#3', 'c': 'E3',
        'v': 'F3', 'g': 'F#3', 'b': 'G3', 'h': 'G#3', 'n': 'A3', 'j': 'A#3', 'm': 'B3',

        # Mid octave (C4–B4)
        'q': 'C4', '2': 'C#4', 'w': 'D4', '3': 'D#4', 'e': 'E4',
        'r': 'F4', '5': 'F#4', 't': 'G4', '6': 'G#4', 'y': 'A4', '7': 'A#4', 'u': 'B4',

        # Upper octave (C5–E5)
        'i': 'C5', '9': 'C#5', 'o': 'D5', '0': 'D#5', 'p': 'E5'
    }

    return render(request, 'pages/play.html', {
        'key_note_map': key_note_map
    })


@login_required
def class_view(request, slug):
    return render(request, template_name='pages/class.html',
                  context={'class': get_object_or_404(MaestroClass, slug=slug)})


@login_required
def lesson_view(request, class_slug, lesson_slug):
    lesson = get_object_or_404(MaestroLesson, slug=lesson_slug)
    assignments = MaestroAssignment.objects.filter(lesson=lesson)  # Fetch assignments for this lesson
    return render(request, 'pages/lesson.html', {'lesson': lesson, 'assignments': assignments})


@teacher_required
def assignment_create_edit(request, class_slug, lesson_slug, assignment_slug=None):
    assignment = None
    lesson = None
    maestro_class = None

    if assignment_slug:
        assignment = get_object_or_404(MaestroAssignment, slug=assignment_slug)
        lesson = assignment.lesson
        maestro_class = lesson.associated_class

        if not (is_admin(request.user) or request.user in maestro_class.teachers.all()):
            messages.error(request, "You do not have permission to edit this assignment.")
            return redirect("find_classes")
    else:
        lesson = get_object_or_404(MaestroLesson, slug=lesson_slug)
        maestro_class = lesson.associated_class

        if not (is_admin(request.user) or request.user in maestro_class.teachers.all()):
            messages.error(request, "You do not have permission to create an assignment.")
            return redirect("find_classes")

    if request.method == "POST":
        form = CreateUpdateAssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)

            if not assignment_slug:
                assignment.lesson = lesson

            assignment.save()

            for student in maestro_class.students.all():
                if assignment not in student.assignments.all():
                    student.assignments.add(assignment)

            create_notification(
                users=maestro_class.students.all(),
                title="New Assignment Added",
                message=f"A new assignment '{assignment.title}' has been added to {maestro_class.title}.",
                notification_type="assignment_added",
                related_object=assignment
            )
            messages.success(request, "Assignment successfully saved and assigned to students.")

            return redirect("assignment_view", class_slug=assignment.lesson.associated_class.slug,
                            lesson_slug=lesson_slug, assignment_slug=assignment.slug)
    else:
        form = CreateUpdateAssignmentForm(instance=assignment)
    return render(request, "pages/create_edit_assignment.html", {"form": form, "assignment": assignment, "lesson": lesson})


def assignment_view(request, class_slug, lesson_slug, assignment_slug):
    return render(request, template_name='pages/assignment.html',
                  context={'assignment': get_object_or_404(MaestroAssignment,
                                                           slug=assignment_slug)})


@teacher_required
def remove_assignment(request, assignment_slug):
    assignment = get_object_or_404(MaestroAssignment, slug=assignment_slug)
    lesson = assignment.lesson

    if not (is_admin(request.user) or request.user in lesson.associated_class.teachers.all()):
        messages.error(request, "You do not have permission to remove this assignment.")
        return redirect("assignment_detail", assignment_slug=assignment.slug)

    # Delete the assignment
    assignment.delete()
    messages.success(request, f"Assignment '{assignment.title}' has been removed.")

    return redirect("lesson_view", class_slug=lesson.associated_class.slug, lesson_slug=lesson.slug)


@admin_required
def class_edit(request, slug=None):
    if slug:
        maestro_class = get_object_or_404(MaestroClass, slug=slug)
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

    return render(request, "pages/create_edit_class.html", {"form": form, "maestro_class": maestro_class})


@teacher_required
def lesson_create_edit(request, class_slug, lesson_slug=None):
    maestro_class = get_object_or_404(MaestroClass, slug=class_slug)

    if lesson_slug:
        maestro_lesson = get_object_or_404(MaestroLesson, slug=lesson_slug, associated_class=maestro_class)
        if not (is_admin(request.user) or request.user in maestro_lesson.associated_class.teachers.all()):
            return redirect("find_classes")
    else:
        # Creating a new lesson
        if not (is_admin(request.user) or request.user in maestro_class.teachers.all()):
            return redirect("find_classes")

        maestro_lesson = None

    if request.method == "POST":
        form = CreateUpdateLessonForm(request.POST, instance=maestro_lesson)
        if form.is_valid():
            maestro_lesson = form.save(commit=False)
            maestro_lesson.associated_class = maestro_class
            if not maestro_lesson.slug:
                maestro_lesson.slug = slugify(maestro_lesson.title)
            maestro_lesson.save()

            create_notification(
                users=maestro_class.students.all(),
                title="New Lesson Added",
                message=f"A new lesson '{maestro_lesson.title}' has been added to {maestro_class.title}.",
                notification_type="lesson_added",
                related_object=maestro_lesson
            )

            return redirect("lesson_view", class_slug=maestro_class.slug, lesson_slug=maestro_lesson.slug)
    else:
        form = CreateUpdateLessonForm(instance=maestro_lesson)

    return render(request, "pages/create_edit_lesson.html", {
        "form": form,
        "maestro_lesson": maestro_lesson,
        "maestro_class": maestro_class
    })


@teacher_required
def remove_lesson(request, class_slug, lesson_slug):
    lesson = get_object_or_404(MaestroLesson, slug=lesson_slug)
    maestro_class = lesson.associated_class

    if not (is_admin(request.user) or request.user in maestro_class.teachers.all()):
        messages.error(request, "You do not have permission to delete this lesson.")
        return redirect("lesson_view", class_slug=class_slug, lesson_slug=lesson_slug)

    lesson.delete()
    messages.success(request, f"Lesson '{lesson.title}' has been deleted.")

    return redirect("class_view", slug=class_slug)


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
    user_notifications = (
        UserNotificationStatus.objects
        .filter(user=request.user)
        .select_related("notification")
        .order_by("notification__created_at")
    )

    return render(
        request,
        "pages/notifications.html",
        context={"notifications": user_notifications}
    )


@teacher_required
def enroll_students(request, class_slug):
    maestro_class = get_object_or_404(MaestroClass, slug=class_slug)

    if not (is_admin(request.user) or request.user in maestro_class.teachers.all()):
        return redirect("find_classes")

    if request.method == "POST":
        form = EnrollStudentsForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data["student"]
            maestro_class.students.add(student)
            student.instruments.add(maestro_class.instrument)
            student.classes.add(maestro_class)

            create_notification(
                users=student,
                title="Enrolled in a Class",
                message=f"You have been added to the class: {maestro_class.title}.",
                notification_type="class_added",
                related_object=maestro_class
            )

            return redirect("class_view", slug=maestro_class.slug)
    else:
        form = EnrollStudentsForm()

    return render(request, "pages/enroll_students.html", {"form": form, "maestro_class": maestro_class})


@teacher_required
def remove_student(request, class_slug, student_username):
    maestro_class = get_object_or_404(MaestroClass, slug=class_slug)
    student = get_object_or_404(MaestroUser, username=student_username)

    if not (is_admin(request.user) or request.user in maestro_class.teachers.all()):
        messages.error(request, "You do not have permission to remove students.")
        return redirect("class_view", slug=class_slug)

    if student in maestro_class.students.all():
        maestro_class.students.remove(student)
        student.classes.remove(maestro_class)
        create_notification(
            users=student,
            title="Removed from Class",
            message=f"You have been removed from the class: {maestro_class.title}.",
            notification_type="class_removed",
            related_object=maestro_class
        )

        messages.success(request, f"{student.username} has been removed from {maestro_class.title}.")
    else:
        messages.warning(request, "This student is not in the class.")

    return redirect("class_view", slug=class_slug)


@login_required
@csrf_exempt
def mark_as_read(request, notification_id):
    if request.method == "POST":
        try:
            user_notification = UserNotificationStatus.objects.get(user=request.user, id=notification_id)
            user_notification.is_read = True
            user_notification.save()

            return JsonResponse({"success": True, "message": "Notification marked as read"}, status=200)
        except UserNotificationStatus.DoesNotExist:
            return JsonResponse({"error": "Notification not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)


