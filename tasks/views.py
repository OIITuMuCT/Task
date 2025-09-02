from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Task
from .mixins import SprintTaskMixin


class TaskListView(ListView):
    """A view that display a list of objects from a Task model"""

    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"


class TaskDetailView(DetailView):
    """A view shows a single object adn its details"""

    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"


class TaskCreateView(SprintTaskMixin, CreateView):
    """A view that shows a form for creating a new object, which is saved to a model"""

    model = Task
    template_name = "task_form.html"
    fields = ("name", "description", "start_date", "end_date")

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.object.id})


class TaskUpdateView(SprintTaskMixin, UpdateView):
    """A view that shows a form for updating an existing object, which is saved to a model"""

    model = Task
    template_name = "task_form.html"
    fields = ("name", "description", "start_date", "end_date")

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.object.id})


class TaskDeleteView(DeleteView):
    """A view that shows a confirmation page and deletes an existing object."""

    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("task-list")
