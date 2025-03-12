from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.utils.text import slugify


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
    duration = models.IntegerField()  # duration in weeks
    capacity = models.IntegerField(default=20)
    instrument = models.ForeignKey(
        MaestroInstrument,
        on_delete=models.CASCADE,
        related_name="classes",
        default=1
    )
    available = models.BooleanField(default=True)
    teachers = models.ManyToManyField(
        "MaestroUser",
        related_name="teaching_classes",
        blank=True
    )
    is_group = models.BooleanField(default=0)
    slug = models.SlugField(unique=True, blank=True)  # Slug field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

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
    slug = models.SlugField(unique=True, blank=True)  # Slug field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MaestroAssignment(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1000)
    date_due = models.DateTimeField()
    lesson = models.ForeignKey(MaestroLesson, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)  # Slug field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class MaestroUser(AbstractUser):
    balance = models.DecimalField(decimal_places=3, max_digits=7, default=0)
    instruments = models.ManyToManyField(MaestroInstrument, related_name="users", blank=True)
    classes = models.ManyToManyField(MaestroClass, related_name="users", blank=True)
    assignments = models.ManyToManyField(MaestroAssignment, related_name="users", blank=True)

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    class Meta:
        verbose_name = "MaestroUser"
        verbose_name_plural = "MaestroUsers"
