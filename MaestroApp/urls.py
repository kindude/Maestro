
from django.urls import path
from .views import index, about, play, test_dashboard, dashboard, class_edit, find_classes, \
    update_user_profile, notifications, lesson_create_edit, assignments_list_view,assignment_detail_view
from MaestroApp.auth_views import *


urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('play', play, name='play'),
    path('dashboard', dashboard, name='dashboard'),
    path('dashboard/test/', test_dashboard, name='test_dashboard'),
    path('logout/', logout_view, name='logout'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('create-class/', class_edit, name='create_class'),
    path('find-classes/', find_classes, name='find_classes'),
    path('profile/update', update_user_profile, name='update_user_profile'),
    path('notifications', notifications, name='notifications'),
    path('class/<int:class_id>/edit/', class_edit, name='class_edit'),
    path('class/<int:class_id>/lesson/<int:lesson_id>/assignment/<int:assignment_id>/', assignment_detail_view, name='assignment_detail'),
    path('class/<int:class_id>/create-lesson/', lesson_create_edit, name="lesson_create"),
    path('assignments/', assignments_list_view, name='assignments_list'),



]