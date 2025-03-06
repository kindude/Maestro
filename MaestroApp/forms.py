from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from MaestroApp import models
from .models import testClass, MaestroInstrument, MaestroUser, MaestroClass

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
        fields = ['title', 'duration', 'capacity', 'instrument']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'instrument': forms.Select(attrs={'class': 'form-control'}),
        }