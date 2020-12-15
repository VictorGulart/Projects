from django import forms
from .models import Task
from django_summernote.widgets import SummernoteWidget

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

class TaskRawForm(forms.Form):
    title = forms.CharField(label='', 
            widget = forms.TextInput(attrs={'placeholder':'Title', 'class':'form-control'})
    )

    message = forms.CharField(
            widget = forms.Textarea(attrs={'placeholder':'Notes', 'class':'form-control'})
    )

