from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__iexact='admin').exists()


def is_teacher(user):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__iexact='teacher').exists()


def is_student(user):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__iexact='student').exists()



def teacher_required(view_func):
    decorated_view_func = user_passes_test(is_teacher, login_url='/login/')(view_func)
    return decorated_view_func


def admin_required(view_func):
    decorated_view_func = user_passes_test(is_admin, login_url='/login/')(view_func)
    return decorated_view_func


def student_required(view_func):
    decorated_view_func = user_passes_test(is_student, login_url='/login/')(view_func)
    return decorated_view_func
