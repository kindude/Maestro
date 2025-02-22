from django.db import models

from django.contrib.auth.models import AbstractUser, Permission, Group


class MaestroRole(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')


def get_default_role():
    return MaestroRole.objects.get_or_create(role="student")[0].id


class MaestroUser(AbstractUser):
    role = models.OneToOneField(MaestroRole, on_delete=models.SET_DEFAULT, default=get_default_role,
                                related_name='user')
    groups = models.ManyToManyField(
        Group,
        related_name="maestro_users_groups",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="maestro_users_permissions",
        blank=True
    )
    password_hash = models.CharField(max_length=256)
    balance = models.DecimalField(decimal_places=3, max_digits=7)

    def __str__(self):
        return self.first_name + self.last_name

