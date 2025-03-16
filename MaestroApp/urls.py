
from django.urls import path
from .views import (index, about, play, dashboard, class_edit, find_classes, \
    update_user_profile, notifications, lesson_create_edit, class_view, lesson_view, assignment_create_edit, 
                    assignment_view, enroll_students, remove_student, remove_assignment, remove_lesson, mark_as_read)
from MaestroApp.auth_views import *


urlpatterns = [

    # pages urls
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard', dashboard, name='dashboard'),

    # auth urls
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),


    path('profile/update', update_user_profile, name='update_user_profile'),
    path('notifications', notifications, name='notifications'),


    # class urls
    path('class/<slug:slug>/', class_view, name='class_view'),
    path('create-class/', class_edit, name='create_class'),
    path('class/<slug:slug>/edit/', class_edit, name='class_edit'),
    path('find-classes/', find_classes, name='find_classes'),

    # lesson urls
    path('class/<slug:class_slug>/create-lesson/', lesson_create_edit, name="lesson_create"),
    path('class/<slug:class_slug>/lesson/<slug:lesson_slug>/', lesson_view, name='lesson_view'),
    path('class/<slug:class_slug>/lesson/<slug:lesson_slug>/edit', lesson_create_edit, name='lesson_edit'),
    path('class/<slug:class_slug>/lesson/<slug:lesson_slug>/remove', remove_lesson, name='remove_lesson'),

    # assignment urls
    path('class/<slug:class_slug>/lesson/<slug:lesson_slug>/create-assignment', assignment_create_edit, name='create_assignment'),
    path('class/<slug:class_slug>/lesson/<slug:lesson_slug>/assignment/<slug:assignment_slug>/', assignment_view, name='assignment_view'),
    path('class/<slug:class_slug>/lesson/<slug:lesson_slug>/assignment/<slug:assignment_slug>/edit', assignment_create_edit, name='assignment_edit'),
    path('assignment/remove/<slug:assignment_slug>/', remove_assignment, name='remove_assignment'),

    # enroll student
    path('profile/enroll-students/<slug:class_slug>/', enroll_students, name='enroll_students'),
    path('class/<slug:class_slug>/remove-student/<str:student_username>/', remove_student, name='remove_student'),

    # notifications
    path('notifications/mark-as-read/<int:notification_id>/', mark_as_read,
         name='mark_as_read'),
    ]
