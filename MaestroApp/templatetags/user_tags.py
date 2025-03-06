from django import template

register = template.Library()

@register.filter
def is_student(user):
    return user.groups.filter(name__iexact='student').exists()


@register.filter
def is_admin(user):
    return user.groups.filter(name__iexact='admin').exists()

@register.filter
def is_teacher(user):
    return user.groups.filter(name__iexact='teacher').exists()

