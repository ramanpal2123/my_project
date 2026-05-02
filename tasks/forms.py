from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = ['title', 'description', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class':       'form-control form-control-lg',
                'placeholder': 'Enter task title...',
            }),
            'description': forms.Textarea(attrs={
                'class':       'form-control',
                'placeholder': 'Add a description (optional)...',
                'rows':        3,
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
        }