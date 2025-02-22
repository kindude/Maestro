from django.db import models

# Create your models here.
# from django.contrib.auth.models import AbstractUser
#
#
# class MaestroUser(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student'),
#     )
#
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
#     classes = models.ManyToManyField('MaestroClass', related_name='users', blank=True)
#
#     def __str__(self):
#         return self.first_name + self.last_name
#
#
# class MaestroClass(models.Model):
#     title = models.CharField(max_length=100)
#
#     teacher = models.ForeignKey(
#         'MaestroUser',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='teaching_classes',
#         limit_choices_to={'role': 'teacher'}
#     )
#
#     students = models.ManyToManyField(
#         'MaestroUser',
#         related_name='enrolled_classes',
#         blank=True,
#         limit_choices_to={'role': 'student'}
#     )
#
#     def __str__(self):
#         return self.title
