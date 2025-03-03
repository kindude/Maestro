from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from MaestroApp import models
from .models import testClass

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
class createClassForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    lesson_duration: int = ...
    instrument= forms.CharField(required=True)
    teacher= forms.CharField(required=True)
    price= forms.IntegerField(required=True)
    is_group= forms.BooleanField(required=True)
    capacity= forms.IntegerField(required=True)
    availability=forms.BooleanField(required=True)
    class Meta:
        model = User
        fields = ['title', 'start_date', 'end_date', 'lesson_duration', 
                  'instrument', 'teacher', 'price', 'is_group', 'capacity', 'availability']

class createModelClass(forms.ModelForm):
    class Meta:
        model = testClass
        fields = "__all__"