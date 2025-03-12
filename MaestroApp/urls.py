
from django.urls import path
from .views import index, about, play, dashboard, class_edit, find_classes, \
    update_user_profile, notifications, lesson_create_edit, class_view, lesson_view
from MaestroApp.auth_views import *


urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('create-class/', class_edit, name='create_class'),
    path('find-classes/', find_classes, name='find_classes'),
    path('profile/update', update_user_profile, name='update_user_profile'),
    path('notifications', notifications, name='notifications'),
    path('class/<slug:slug>/', class_view, name='class_view'),
    path('class/<slug:slug>/edit/', class_edit, name='class_edit'),


    # lesson urls
    path('class/<slug:class_slug>/create-lesson/', lesson_create_edit, name="lesson_create"),
    path('class/<slug:class_slug>/lesson/<slug:lesson_slug>/', lesson_view, name='lesson_view'),
    path('class/<slug:class_slug>/lesson/<slug:lesson_slug>/edit', lesson_create_edit, name='lesson_edit'),
]