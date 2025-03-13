from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from MaestroApp import models
from .models import MaestroInstrument, MaestroUser, MaestroClass, MaestroLesson, MaestroAssignment
from django.core.exceptions import ValidationError
User = get_user_model()


# Registration Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# Class Create Form
class CreateClassForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    lesson_duration: int = forms.IntegerField()
    instrument = forms.ModelChoiceField(
        queryset=MaestroInstrument.objects.all(),
        empty_label="Select an Instrument",
        required=True)
    teacher = forms.ModelChoiceField(
        queryset=MaestroUser.objects.filter(groups__name__iexact='teacher'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    price = forms.IntegerField(required=True)
    is_group = forms.BooleanField(required=True)
    capacity = forms.IntegerField(required=True)
    availability = forms.BooleanField(required=True)
    class Meta:
        model = User
        fields = ['title', 'start_date', 'end_date', 'lesson_duration', 
                  'instrument', 'teacher', 'price', 'is_group', 'capacity', 'availability']


class CreateModelClass(forms.ModelForm):
    teacher = forms.ModelMultipleChoiceField(
        queryset=MaestroUser.objects.filter(groups__name__iexact='teacher'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )
    instrument = forms.ModelChoiceField(
        queryset=MaestroInstrument.objects.all(),
        empty_label="Select an Instrument",
        required=True)

    class Meta:
        model = MaestroClass
        fields = ['title', 'duration', 'capacity', 'instrument', 'teacher', 'is_group', 'available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'instrument': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_group': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False, max_length=150)
    last_name = forms.CharField(required=False, max_length=150)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    username = forms.CharField(required=False, max_length=150)

    class Meta:
        model = MaestroUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_username(self):
        """
        Ensure the username is unique before saving.
        """
        username = self.cleaned_data.get('username')
        if username:
            existing_user = MaestroUser.objects.filter(username=username).exclude(pk=self.instance.pk)
            if existing_user.exists():
                raise ValidationError("This username is already taken. Please choose another.")
        return username

class CreateUpdateLessonForm(forms.ModelForm):
    title = forms.CharField(required=False, max_length=200)
    duration = forms.IntegerField()
    is_group = forms.BooleanField()
    price = forms.DecimalField(decimal_places=3, max_digits=7)
    dt = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = MaestroLesson
        fields = ['title', 'duration', 'is_group', 'price', 'dt']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_group': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dt': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class CreateUpdateAssignmentForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter assignment title'}),
        required=True
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter assignment details'}),
        required=True
    )

    date_due = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=True
    )

    attachment = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        required=False
    )

    class Meta:
        model = MaestroAssignment
        fields = ['title', 'text', 'date_due', 'attachment']


class EnrollStudentsForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=MaestroUser.objects.all().order_by("username"),
        empty_label="Select a Student",
        widget=forms.Select(attrs={'class': 'form-control'})
    )