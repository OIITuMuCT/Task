from collections import defaultdict
from datetime import date
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    JsonResponse,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.template import loader

from .models import Task
from .mixins import SprintTaskMixin
from . import services
from .forms import TaskForm, ContactForm, EpicFormSet

# Added LoginRequiredMixin for authenticate user
class TaskListView(PermissionRequiredMixin, ListView):
    """A view that display a list of objects from a Task model"""
    permission_required = ("task.view_task", "tasks.custom_task")
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"
    login_url = '/login/'
    raise_exception = True


class TaskDetailView(DetailView):
    """A view shows a single object adn its details"""
    # permission_required = 'tasks.view_task'
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    """A view that shows a form for creating a new object, which is saved to a model"""
    permission_required = ("task_add")
    model = Task
    template_name = "tasks/task_form.html"
    # fields = ("title", "description")
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        # Set the creator to the currently logged in user
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(PermissionRequiredMixin, SprintTaskMixin, UpdateView):
    """A view that shows a form for updating an existing object, which is saved to a model"""
    permission_required = ("tasks.change_task",)
    model = Task
    template_name = "tasks/task_form.html"
    fields = ("title", "description")

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.id})

    def has_permission(self):
        # First, check if the user has the general permission to edit tasks
        has_general_permission = super().has_permission()
        
        # Then check if the user is either the
        # creator or teh owner of this task
        task_id = self.kwargs.get("pk")
        task = get_object_or_404(Task, id=task_id)
        
        is_creator_or_owner = (
            task.creator == self.request.user or task.owner == self.request.user
        )
        
        # Return True only if both conditions are met
        return has_general_permission and is_creator_or_owner

class TaskDeleteView(DeleteView):
    """A view that shows a confirmation page and deletes an existing object."""

    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task-list")


# @login_required
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


def task_by_date(request: HttpRequest, by_date: date) -> HttpResponse:
    tasks = services.get_task_by_date(by_date)
    context = {"tasks": tasks}
    return render(request, "tasks/task_list.html", context)


def example_view(request):
    template = loader.get_template("tasks/example.html")
    context = {"name": "Test"}
    html = template.render(context, request)
    return HttpResponse(html)

def contact_form_view(request):
    """ Send to email form """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']
            services.send_contact_email(subject, message, from_email, 'your-email@example.com')
            return redirect(reverse('tasks:contact-success'))
    else:
        form = ContactForm()
    return render(request, 'tasks/example_form.html', {'form': form})
    # return render(request, "tasks/example.html", {"form": form})


@permission_required("tasks.add_task")
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

@login_required
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

        # You can use Django's send_mail function,
        # here is a simple example that sends the message to your email.
        # Please update 'your-email@example.com' with your email and configure
        # the EMAIL settings in your Django settings file
        services.send_contact_email(
            subject, message, from_email, ["your-email@example.com"]
        )

        return super().form_valid(form)

@login_required
def manage_epic_tasks(request, epic_pk):
    epic = services.get_epic_by_id(epic_pk)
    if not epic:
        raise Http404('Epic does not exist')
    if request.method == "POST":
        formset = EpicFormSet(request.POST, queryset=services.get_tasks_for_epic(epic))
        if formset.is_valid():
            tasks = formset.save(commit=False)
            services.save_tasks_for_epic(epic, tasks)
            formset.save_m2m() # Handle many-to-many relations if there are any
            return redirect('tasks:task-list')
    else:
        formset = EpicFormSet(queryset=services.get_tasks_for_epic(epic))
    return render(request, 'tasks/manage_epic.html', {'formset': formset, 'epic': epic})
