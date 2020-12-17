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


class CreateUserForm(UserCreationForm):
        username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
        email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'*****'}))
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'*****'}))


        class Meta:
                model = User

                fields = [
                        'username', 'email', 'password1', 'password2'
                ]