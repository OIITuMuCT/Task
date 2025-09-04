from django.urls import path, register_converter
from django.views.generic import TemplateView

from . import views, converters

from .views import (
    TaskListView,
    TaskDeleteView,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
    ContactFormView,
    example_view,
    task_by_date,
    task_home,
    contact_form_view,
    manage_epic_tasks
)

app_name = "tasks"  # This is for namespacing the URLs
register_converter(converters.DateConverter, "yyyymmdd")
urlpatterns = [
    path("", TemplateView.as_view(template_name="tasks/home.html"), name="home"),
    path("help/", TemplateView.as_view(template_name="tasks/help.html"), name="help"),
    path("tasks/", TaskListView.as_view(), name="task-list"),  # GET
    path("tasks/<yyyymmdd:date>/", task_by_date),
    path("example/", example_view, name="example"),
    path('example-form/', contact_form_view, name='example-form'),
    path("tasks/new/", TaskCreateView.as_view(), name="task-create"),  # POST
    path("tasks/home/", task_home, name="task-home"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-update"
    ),  # PUT/PATCH
    path(
        "tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"
    ),  # DELETE
    path(
        "tasks/sprint/add_task/<int:pk>/",
        views.create_task_on_sprint,
        name="task-add-to-sprint",
    ),
    path("contact/", ContactFormView.as_view(), name="contact"),
    path(
        "contact-success/",
        TemplateView.as_view(template_name="tasks/contact_success.html"),
        name="contact-success",
    ),
    path("epic/<int:epic_pk>/", manage_epic_tasks, name="task-batch-create"),
]
