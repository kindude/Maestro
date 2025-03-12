from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from MaestroApp import models
from .models import  MaestroInstrument, MaestroUser, MaestroClass, MaestroLesson

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

    class Meta:
        model = MaestroUser
        fields = ['first_name', 'last_name', 'date_of_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CreateUpdateLessonForm(forms.ModelForm):
    title = forms.CharField(required=False, max_length=200)
    duration = forms.IntegerField()
    is_group = forms.BooleanField()
    price = forms.DecimalField(decimal_places=3, max_digits=7)
    dt = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    associated_class = forms.ModelChoiceField(
        queryset=MaestroClass.objects.all(),
        empty_label="Select a Class",
        required=True)

    class Meta:
        model = MaestroLesson
        fields = ['title', 'duration', 'is_group', 'price', 'dt', 'associated_class']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_group': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dt': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'associated_class': forms.Select(attrs={'class': 'form-control'}),
        }