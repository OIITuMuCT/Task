import uuid
from django import forms
from django.forms import modelformset_factory
# from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError,transaction
from .models import FormSubmission, SubscribedEmail, Task
from tasks.fields import EmailsListField

class TaskForm(forms.ModelForm):
    """Form for create Task"""
    uuid = forms.UUIDField(required=False, widget=forms.HiddenInput())
    watchers = EmailsListField(required=False)

    class Meta:
        model = Task
        fields = ["title", "description", "status", "watchers", "file_upload", "image_upload"]

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Check if an instance is provided and populate watchers field
        if self.instance and self.instance.pk:
            self.fields['watchers'].initial = ', '.join(email.email for email in self.instance.watchers.all())
        self.fields['uuid'].initial = uuid.uuid4()

    def clean_uuid(self):
        uuid_value = str(self.cleaned_data.get("uuid"))
        # was_set = cache.set(uuid_value, "submitted", nx=True)
        # if not was_set:
        #     # If 'was_set' is False, the UUID already exists in the cache.
        #     raise ValidationError("This form has already been submitted.")
        with transaction.atomic():
            # Try to record the form submission by UUID
            try:
                FormSubmission.objects.create(uuid=uuid_value)
            except IntegrityError:
                # The UUID already exists, so the form was already submitted
                raise ValidationError("This form has already been submitted.")
        return uuid_value

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

EpicFormSet = modelformset_factory(Task, form=TaskForm, extra=0)
