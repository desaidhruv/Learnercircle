from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import CompetitionRegistration

class RegisterForm(UserCreationForm):
    email = forms.EmailField() #adding email field
    
    class Meta:
        model = User
        fields = ["username","email","password1","password2"] #order of fields

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = CompetitionRegistration
        fields = "__all__"