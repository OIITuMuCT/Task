from collections import defaultdict
from datetime import date
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    JsonResponse,
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.template import loader
from datetime import date

from .models import Task
from .mixins import SprintTaskMixin
from . import services
from .services import create_task_and_add_to_sprint
from .forms import TaskForm, ContactForm


class TaskListView(ListView):
    """A view that display a list of objects from a Task model"""

    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"


class TaskDetailView(DetailView):
    """A view shows a single object adn its details"""

    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(CreateView):
    """A view that shows a form for creating a new object, which is saved to a model"""

    model = Task
    template_name = "tasks/task_form.html"
    # fields = ("title", "description")
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.object.id})


class TaskUpdateView(SprintTaskMixin, UpdateView):
    """A view that shows a form for updating an existing object, which is saved to a model"""

    model = Task
    template_name = "tasks/task_form.html"
    fields = ("title", "description")

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.id})


class TaskDeleteView(DeleteView):
    """A view that shows a confirmation page and deletes an existing object."""

    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task-list")


def task_by_date(request: HttpRequest, by_date: date) -> HttpResponse:
    tasks = services.get_task_by_date(by_date)
    context = {"tasks": tasks}
    return render(request, "tasks/task_list.html", context)


def task_home(request):
    # Fetch all tasks at once
    tasks = Task.objects.filter(
        status__in=["UNASSIGNED", "IN_PROGRESS", "DONE", "ARCHIVED"]
    )
    # initialize dictionaries to hold tasks by status
    context = defaultdict(list)
    # Categorize tasks into their respective lists for task in tasks:
    for task in tasks:
        if task.status == "UNASSIGNED":
            context["unassigned_tasks"].append(task)
        elif task.status == "IN_PROGRESS":
            context["in_progress_tasks"].append(task)
        elif task.status == "DONE":
            context["done_tasks"].append(task)
        elif task.status == "ARCHIVED":
            context["archived_tasks"].append(task)
    # return redirect(reverse("tasks:task-list"))
    return render(request, "tasks/home.html", context)


def example_view(request):
    template = loader.get_template("tasks/example.html")
    context = {"name": "Test"}
    html = template.render(context, request)
    return HttpResponse(html)


def create_task_on_sprint(request: HttpRequest, sprint_id: int) -> HttpResponseRedirect:
    if request.method == "POST":
        task_data: dict[str, str] = {
            "title": request.POST["title"],
            "description": request.POST.get("description", ""),
            "status": request.POST.get("status", "UNASSIGNED"),
        }
        task = services.create_task_and_add_to_sprint(
            task_data, sprint_id, request.user
        )
        return redirect("tasks:task-detail", task_id=task.id)
    raise Http404("Not found")


def claim_task_view(request, task_id):
    user_id = (
        request.user.id
    )  # Assuming you have access to the user ID from the request

    try:
        services.claim_task(user_id, task_id)
        return JsonResponse({"message": "Task successfully claimed."})
    except Task.DoesNotExist:
        return HttpResponse("Task does not exist.", status=404)
    except services.TaskAlreadyClaimedException:
        return HttpResponse("Task does not exist.", status=400)


def custom_404(request, exception):
    return render(request, "404.html", {}, status=404)



class ContactFormView(FormView):
    template_name = "tasks/contact_form.html"
    form_class = ContactForm
    success_url = reverse_lazy("tasks:contact-success")

    def form_valid(self, form):
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        from_email = form.cleaned_data.get("from_email")
        services.send_contact_email(
            subject, message, from_email, ["your-email@example.com"]
        )
        return super().form_valid(form)
