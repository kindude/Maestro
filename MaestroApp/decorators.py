from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_teacher(user):
    return user.groups.filter(name="Teacher").exitsts()


def is_student(user):
    if not user.is_authenticated:
        return False  # User must be logged in

    user.refresh_from_db()  # Force refresh from database
    print("User Groups after refresh:", user.groups.values_list("name", flat=True))  # Debugging

    return user.groups.filter(name="Student").exists()



def teacher_required(view_func):
    decorated_view_func = user_passes_test(is_teacher, login_url='/login/')(view_func)
    return decorated_view_func


def admin_required(view_func):
    decorated_view_func = user_passes_test(is_admin, login_url='/login/')(view_func)
    return decorated_view_func


def student_required(view_func):
    decorated_view_func = user_passes_test(is_student, login_url='/login/')(view_func)
    return decorated_view_func
