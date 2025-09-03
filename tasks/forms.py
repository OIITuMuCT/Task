from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Form for create Task"""

    class Meta:
        model = Task
        fields = ["title", "description", "status"]
