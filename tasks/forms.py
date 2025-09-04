from django import forms
from .models import SubscribedEmail, Task
from tasks.fields import EmailsListField

class TaskForm(forms.ModelForm):
    """Form for create Task"""
    watchers = EmailsListField(required=False)

    class Meta:
        model = Task
        fields = ["title", "description", "status", "watchers"]

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Check if an instance is provided and populate watchers field
        if self.instance and self.instance.pk:
            self.fields['watchers'].initial = ', '.join(email.email for email in self.instance.watchers.all())

    def save(self, commit=True):
        # First, save the Task instance
        task = super().save(commit)
        # If commit is True, save the associated emails
        if commit:
            # First, remove the old emails associated with this task
            task.watchers.all().delete()
        # Add the new emails to the Email model
        for email_str in self.cleaned_data['watchers']:
            SubscribedEmail.objects.create(email=email_str, task=task)
        return task


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
