from django import forms
from .models import Task
from django.forms import Textarea, TextInput, EmailField, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task

        fields = [
                'title', 'message'
                ]
        widgets = {
            'title':forms.TextInput(attrs={'placeholder':'Title', 'class':'form-control'}),
            'message':forms.Textarea(attrs={'placeholder':'Notes', 'class':'form-control'})
        }



