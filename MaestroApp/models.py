from django.db import models
from typing import Optional
from django.contrib.auth.models import AbstractUser, Permission, Group


class MaestroRole(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.get_role_display()

def get_default_role():
    return MaestroRole.objects.get_or_create(role='student')


class MaestroInstrument(models.Model):
    INSTRUMENT_CHOICES = (
        ('violin', 'Violin'),
        ('guitar', 'Guitar'),
        ('piano', 'Piano'),
        ('drums', 'Drums')
    )
    instrument = models.CharField(max_length=10, choices=INSTRUMENT_CHOICES)

    def __str__(self):
        return self.get_instrument_display()


class MaestroClass(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField() # duration in weeks
    capacity = models.IntegerField(default=20)
    instrument = models.ForeignKey(
        MaestroInstrument,
        on_delete=models.CASCADE,
        related_name="classes",
        default=1
    )
    
    def __str__(self):
        return self.title

class testClass(models.Model):
    title = models.CharField(max_length = 200)
    instrument= models.CharField(max_length = 200)
    teacher= models.CharField(max_length = 200)
    price= models.IntegerField()
    is_group= models.BooleanField(default = False)
    capacity= models.IntegerField(default = 20)
    availability=models.BooleanField(default = True)
    def __str__(self):
        return self.title

class MaestroLesson(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField(default=60) # duration in minutes
    is_group = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=3, max_digits=7)
    dt = models.DateTimeField()
    associated_class = models.ForeignKey(
        MaestroClass,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    def __str__(self):
        return self.title


class MaestroAssignment(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1000)
    date_due = models.DateTimeField()
    lesson = models.ForeignKey(
        MaestroLesson,
        on_delete=models.CASCADE,
        related_name="assignments"
    )


class RoleMixin:
    role: Optional[MaestroRole]

    def is_admin(self):
        return self.role and self.role.role == 'admin'

    def is_teacher(self):
        return self.role and self.role.role == 'teacher'

    def is_student(self):
        return self.role and self.role.role == 'student'


class MaestroUser(AbstractUser, RoleMixin):
    role = models.ForeignKey(
        MaestroRole,
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name='users'
    )
    balance = models.DecimalField(decimal_places=3, max_digits=7, default=0)
    instruments = models.ManyToManyField(MaestroInstrument, related_name="users", blank=True)
    classes = models.ManyToManyField(MaestroClass, related_name="users", blank=True)
    assignments = models.ManyToManyField(MaestroAssignment, related_name="users", blank=True)

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username



