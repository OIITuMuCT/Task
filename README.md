# Task Manager

- [1. Creating a **_Task_** model](#1-creating-a-task-model)
  - [Extending the models](#extending-the-models)
- [2. Django's database API: Create, retrieve, update, and delete operations](#2-djangos-database-api-create-retrieve-update-and-delete-operations)
- [3. Django's admin interface: Registering models and manipulating data](#3-djangos-admin-interface-registering-models-and-manipulating-data)
- [4. Introduction to Django's ORM: Queries and aggregations](#4-introduction-to-djangos-orm-queries-and-aggregations)

- [5. Django Views and URL Handling](#5-django-views-and-url-handling)

  - [Introduction to Django's Generic Views](#introduction-to-djangos-generic-views)
  - [Writing Your First Django View](#writing-your-first-django-view)
    <details>
    <summary>Click to expand</summary>

    - [TaskListView](#tasklistview)
    - [TaskDetailView](#taskdetailview)
    - [TaskCreateView](#taskcreateview)
    - [TaskUpdateView](#taskupdateview)
    - [TaskDeleteView](#taskdeleteview)

    </details>

  - [Class-based Views Mixins](#class-based-views-mixins)
    - [Attribute Mixin](#attribute-mixin)
    - [Data Modification Mixin](#data-modification-mixin)
    - [Fetching data](#fetching-data)
    - [Redirect and Success URL Handling](#redirect-and-success-url-handling)
  - [URL Configuration in Django](#url-configuration-in-django)
  - [Creating URL Patterns for Your Views](#creating-url-patterns-for-your-views)
  - [Using Django’s HttpRequest and HttpResponse Objects](#using-djangos-httprequest-and-httpresponse-objects)
  - [Handling Dynamic URLs with Path Converters](#handling-dynamic-urls-with-path-converters)
  - [Understanding Django’s URL Namespace and Naming URL Patterns](#understanding-djangos-url-namespace-and-naming-url-patterns)
  - [Introduction to Function-based Views](#introduction-to-function-based-views)
  - [Using Function-based Views with a Service Layer](#using-function-based-views-with-a-service-layer)
  - [Pessimistic and Optimistic Locking Using Views and a Service Layer](#pessimistic-and-optimistic-locking-using-views-and-a-service-layer)
  - [Error Handling with Custom Error Views](#error-handling-with-custom-error-views)

- [6. Using the Django Template Engine](#6-using-the-django-template-engine)
  - [Introduction to Django Template Engine](#introduction-to-django-template-engine)
  - [Creating Your First Django Template](#creating-your-first-django-template)
  - [Django Template Language: Variables, Tags, and Filters](#django-template-language-variables-tags-and-filters)
  - [Using Static Files in Django Templates: CSS, JavaScript, Images](#using-static-files-in-django-templates-css-javascript-images)
  - [Inheritance in Django Templates](#inheritance-in-django-templates)
  - [Including Templates: Reusing Template Code](#including-templates-reusing-template-code)
  - [The home page view: Showing Tasks by status](#the-home-page-view-showing-tasks-by-status)
  - [Custom Template Tags and Filters](#custom-template-tags-and-filters)
  - [Django Template Context Processors](#django-template-context-processors)
  - [Debugging Django Templates](#debugging-django-templates)
  - [Optimizing Template Rendering](#optimizing-template-rendering)
  - [Securing Django Templates](#securing-django-templates)

- [7. Forms in Django](#7-forms-in-django)
  - [Understanding Django Forms](#understanding-django-forms)
  - [Creating Your First Django Form](#creating-your-first-django-form)
  - [Rendering Forms in Templates](#rendering-forms-in-templates)
  - [Handling Form Submission in Views](#handling-form-submission-in-views)
  - [Working with Form Fields](#working-with-form-fields)
  - [File and Image Upload Field](#file-and-image-upload-field)
  - [Data Validation with Django Forms](#data-validation-with-django-forms)
  - [Displaying Form Errors](#displaying-form-errors)
  - [Advanced Form Handling: ModelForms and Formsets](#advanced-form-handling-modelforms-and-formsets)
  - [Preventing Double Submission with Forms](#preventing-double-submission-with-forms)
## 1. Creating a **_Task_** model

<!--Chapter 1-->
<details>  
<summary>Click to expand</summary>

```python
    from django.db import models
    from django.contrib.auth.models import User


    class Task(models.Model):
        STATUS_CHOICES = [
            ("UNASSIGNED", "Unassigned"),
            ("IN_PROGRESS", "In Progress"),
            ("DONE", "Completed"),
            ("ARCHIVED", "Archived"),
        ]

        title = models.CharField(max_length=250)
        description = (models.TextField(blank=True, null=False, default=""),)
        status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default="UNASSIGNED",
            db_comment="Can be UNASSIGNED, IN_PROGRESS, DONE, or ARCHIVED",
        )

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        creator = models.ForeignKey(
            User, related_name="created_tasks", on_delete=models.CASCADE
        )

        owner = models.ForeignKey(
            User,
            related_name="owned_tasks",
            on_delete=models.SET_NULL,
            null=True,
            db_comment="Foreign Key to the User who currently owns the task.",
        )

        class Meta:
            db_table_comment = "Holds information about tasks"
```

</details>
<!-- end 1 -->
<!--Chapter 2-->

## 2. Django's database API: Create, retrieve, update, and delete operations

<!-- start 2 -->
<!-- end 2 -->
<!--Chapter 3-->
## 3. Django's admin interface: Registering models and manipulating data


- #### Firstly, you need to create an empty migration:

  `shell: python manage.py makemigrations tasks --empty`

- #### Configure the groups from it or create a data migration

<details>  
<summary>Click to expand</summary>

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def create_groups(apps, schema_editor):
    # create "Author" group with "add_task" permission
    Task = apps.get_model("tasks", "Task")
    content_type = ContentType.objects.get_for_model(Task)

    author_group = Group.objects.create(name="Author")
    add_task_permission, _ = Permission.objects.get_or_create(
        codename="add_tasks", content_type=content_type
    )
    author_group.permissions.add(add_task_permission)

    # create "Editor" group with "change_task" permission
    editor_group = Group.objects.create(name="Editor")
    change_task_permission, _ = Permission.objects.get_or_create(
        codename="change_task", content_type=content_type
    )
    editor_group.permissions.add(change_task_permission)

    # create "Admin" group with all permissions
    admin_group = Group.objects.create(name="Admin")
    all_permissions = Permission.objects.filter(content_type__app_label="tasks")
    admin_group.permissions.set(all_permissions)


class Migration(migrations.Migration):
    dependencies = [
        (
            "tasks",
            "0002_move_archived_to_done",
        ),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
```

</details>
<!-- end 3 -->
<!--Chapter 4-->
## 4. Introduction to Django's ORM: Queries and aggregations


- ### Django uses the double underscore is a notation to indicate a separation in the query and it could be used to perform comparisons:

  <details>  
  <summary>Click to expand</summary>

  - **gt**: Greater than
  - **gte**: Greater than or equal to
  - **lte**: Less than or equal to
  - **contains**: Field contains the value. Case-sensitive
  - **in**: Within a range
  - **isnull**: is NULL (or not)
  </details>

- ### Extending the models

    <details>  
    <summary>Click to expand</summary>

  - **The One-to-One Relationship(OneToOneField):** A one-to-one relationship
    implies that one object is related to exactly one other object. This can be
    seen as a constrained version of the ForeignKey, where the reverse relation
    is unique.

    ```python
       from django.db import models
       from django.contrib.auth.models import User

       class Profile(models.Model):
           user = models.OneToOneField(User, on_delete=models.CASCADE)
           # Other fields...
    ```

    - **The One-To-Many Relationship(OneToManyField):** A One-To-Many relationship implies one object can be related to several others.

    ```python
    from django.db import models
    from django.contrib.auth.models import User
    class Task(models.Model):
       …
       creator = models.ForeignKey(User,
           related_name='created_tasks',
           on_delete=models.CASCADE)
    ```

    - **The Many-To-Many Relationship(ManyToManyField):** In this relationship, objects can relate to
      several others, which, in turn, can associate with multiple entities.

    ```python
        class Sprint(models.Model):
            name = models.CharField(max_length=200)
            description = models.TextField(blank=True, null=True)
            start_date = models.DateField()
            end_date = models.DateField()
            created_at = models.DateTimeField(auto_now_add=True)
            updated_at = models.DateTimeField(auto_now=True)
            creator = models.ForeignKey(User,
                related_name='created_sprints', on_delete=models.CASCADE)
            tasks = models.ManyToManyField('Task',
                related_name='sprints', blank=True)
    ```

    </details>
<!--Chapter 5-->
## 5. Django Views and URL Handling

- [Introduction to Django's Generic Views](#introduction-to-djangos-generic-views)
- [Writing Your First Django View](#writing-your-first-django-view)
- [Class-based Views Mixins](#class-based-views-mixins)
- [URL Configuration in Django](#url-configuration-in-django)
- [Creating URL Patterns for Your Views](#creating-url-patterns-for-your-view)
- [Using Django’s HttpRequest and HttpResponse Objects](#using-djangos-httprequest-and-httpresponse-objects)
- [Handling Dynamic URLs with Path Converters](#handling-dynamic-urls-with-path-converters)
- [Understanding Django’s URL Namespace and Naming URL Patterns](#understanding-djangos-url-namespace-and-naming-url-patterns)
- [Introduction to Function-based Views](#introduction-to-function-based-views)
- [Using Function-based Views with a Service Layer](#using-function-based-views-with-a-service-layer)
- [Pessimistic and Optimistic Locking Using Views and a Service Layer](#pessimistic-and-optimistic-locking-using-views-and-a-service-layer)
- [Error Handling with Custom Error Views](#error-handling-with-custom-error-views)

### Introduction to Django's Generic Views

<details>  
    <summary>Click to expand</summary>

- List and detail views:

  - **ListView:** A view that displays a list of objects from a model.
  - **DetailView:** A view that show a single objects and its details.

- Date-based views:

  - **ArchiveIndexView:** A date-based view that lists objects from a date-based queryset in the "latest firs" order
  - **YearArchiveView:** A date-based view that lists objects from a year-based queryset.
  - **MonthArchiveView:** A date-based view that list objects form a month-based queryset.
  - **WeekArchiveView:** A date-based view that list objects from a week-based queryset.
  - **DayArchiveView:** A date-based view that list objects from a day-based queryset.
  - **TodayArchiveView:** A date-based view that list objects from a queryset related to the current day.
  - **DateDetailView:** A date-based view that provides an object from a date-based queryset, matching the given year, month, and day.

- Editing views:

  - **FormView:** A view that displays a form on GET and processes it on POST.
  - **CreateView:** A view that shows a form for creating a new object, which is saved to a model.
  - **UpdateView:** A view that shows a form for updating an existing objects, which is saved to a model.
  - **DeleteView:** A view that shows a confirmation page and deletes an existing object.

- The base view:

  - **TemplateView:** A view that renders a specified template. This one does not involve any kind of model operations.
  </details>

### Writing Your First Django View

<details>  
<summary>Click to expand</summary>

#### TaskListView

```python
    from django.views.generic import ListView

    class TaskListView(ListView):
    """A view that display a list from of objects from a model"""
        model = Task
        template_name = 'task_list.html'
        context_object_name = "tasks"
```

#### TaskDetailView

```python
    from django.views.generic import DetailView

    class TaskDetailView(DetailView):
    """A view shows a single object and its details"""
        model = Task
        template_name = 'task_detail.html
        context_object_name = 'task'
```

#### TaskCreateView

```python
    from django.views.generic.edit import CreateView
    from django.urls import reverse_lazy

    class TaskCreateView(CreateView):
        """A view that shows a form for creating a new object, which is saved to a model"""
        model = Task
        template_name = 'task_form.html
        fields = ('name', 'description', 'start_date', 'end_date')
        def get_success_url(self):
            return reverse_lazy('task-detail', kwargs={"pk": self.object.id})
```

#### TaskUpdateView

```python
    from django.views.generic.edit import UpdateView
    from django.urls import reverse_lazy

    class TaskUpdateView(UpdateView):
        """A view that shows a form for updating an existing object, which is saved to a model"""
        model = Task
        template_name = 'task_form.html'
        fields = ('name', 'description', 'start_date', 'end_date')
        def get_success_url(self):
            return reverse_lazy('task-detail', kwargs={"pk": self.object.id})
```

#### TaskDeleteView

```python
    from django.views.generic.edit import DeleteView
    from django.urls import reverse_lazy

    class TaskDeleteView(DeleteView):
        """ A view that shows a confirmation page and deletes an existing object"""
        model = Task
        template_name = 'task_confirm_delete.html'
        success_url = reverse_lazy('task-list')
```

</details>

### Class-based Views Mixins

#### SprintTaskWithinRangeMixin

<details>  
<summary>Click to expand</summary>

```python
from django.http import HttpResponseBadRequest

from .services import can_add_task_to_sprint


class SprintTaskMixin:
    """
    Mixin to ensure a task being created or updated is
    within the date range of its associated sprint.
    """

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object() if hasattr(self, "get_object") else None
        sprint_id = request.POST.get("sprint_id")

        if sprint_id:
            # If task exists (for UpdateView) or
            # is about to be created (for CreateView)
            if task or request.method == "POST":
                if not can_add_task_to_sprint(task, sprint_id):
                    return HttpResponseBadRequest(
                        "Task's creation date is outside the "
                        "date range of the associated sprint."
                    )

        return super().dispatch(request, *args, **kwargs)
```

#### The code for service layer is the following:

```python
def can_add_task_to_sprint(task, sprint_id):
    """
    Checks if a task can be added to a sprint based on the sprint's date range.
    """
    sprint = get_object_or_404(Sprint, id=sprint_id)
    return sprint.start_date <= task.created_at.date() <= sprint.end_date
```

</details>  
<details>  
<summary>Click to expand</summary>

#### Attribute Mixin

- **ContentMixin:** Adds extra content data to the view.
- **TemplateResponseMixin:** Renders template and returns an HTTP response.
- **SingleObjectsMixin:** Provides handling to get a single object from the database.

#### Data Modification Mixin

- **FormMixin:** Used to handle form submission and validation.
- **ModelFormMixin:** Extends FormMixin to deal with model forms.
- **CreateModelMixin:** Used to save a new object to the database.
- **UpdateModelMixin:** Used to update an existing object in the database.
- **DeleteModelMixin:** Used to delete an object.

#### Fetching data

- **SingleObjectMixin:** Used to fetch a single object based on the primary key or slug
- **MultipleObjectsMixin:** Used to fetch multiple objects (often used for listing views)
- **Pagination**
- **MultipleObjectMixin:** Provides pagination functionality if the **paginate_by** attribute is set

#### Redirect and Success URL Handling

- **RedirectView:** Used to handle simple HTTP redirects.
- **SuccessMessageMixin:** Used to display a success message after acting successfully.
</details>

### URL Configuration in Django

### Creating URL Patterns for Your Views

<details>
<summary>Click to expand</summary>

```python
from django.urls import path
from tasks.views import (
    TaskListView,
    TaskDeleteView,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
)
urlpatterns = [
    path("", TemplateView.as_view(template_name="tasks/home.html"), name="home"),
    path("help/", TemplateView.as_view(template_name="tasks/help.html"), name="help"),
    path("tasks/", TaskListView.as_view(), name="task-list"),  # GET
    path("tasks/new/", TaskCreateView.as_view(), name="task-create"),  # POST
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-update"
    ),  # PUT/PATCH
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name='task-delete'), # DELETE
]
```

</details>

### Using Django’s HttpRequest and HttpResponse Objects

### Handling Dynamic URLs with Path Converters

### Understanding Django’s URL Namespace and Naming URL Patterns

### Introduction to Function-based Views

### Using Function-based Views with a Service Layer

### Pessimistic and Optimistic Locking Using Views and a Service Layer

### Error Handling with Custom Error Views
<!--Chapter 6-->
## 6. Using the Django Template Engine

- ### Introduction to Django Template Engine
- ### Creating Your First Django Template
- ### Django Template Language: Variables, Tags, and Filters
- ### Using Static Files in Django Templates: CSS, JavaScript, Images
- ### Inheritance in Django Templates
- ### Including Templates: Reusing Template Code
- ### The home page view: Showing Tasks by status

```python
    def task_home(request):
        # Fetch all tasks at once
        tasks = Task.objects.filter(status__in=["UNASSIGNED",
            "IN_PROGRESS", "DONE", "ARCHIVED"])
        # Initialize dictionaries to hold tasks by status
        context = defaultdict(list)
        # Categorize tasks into their respective lists
        for task in tasks:
        if task.status == "UNASSIGNED":
            context["unassigned_tasks"].append(task)
        elif task.status == "IN_PROGRESS":
            context["in_progress_tasks"].append(task)
        elif task.status == "DONE":
            context["done_tasks"].append(task)
        elif task.status == "ARCHIVED":
            context["archived_tasks"].append(task)
        return render(request, "tasks/home.html", context)
```

- ### Custom Template Tags and Filters
- ### Django Template Context Processors
> tasks/context_processors.py
```python

    from django.contrib.auth.models import Group
    def feature_flags(request):
        user = request.user
        flags = {
            "is_priority_feature_enabled": False,
        }
        # Ensure the user is authenticated before checking groups
        if user.is_authenticated:
            flags["is_priority_feature_enabled"] = user.groups.filter(
                name="Task Prioritization Beta Testers"
            ).exists()
        return flags
```
> When using the feature flag in your template, treat it as a variable:
```html
    {% if is_priority_feature_enabled %}
    <!-- Render UI elements related to task prioritization -->
    {% else %}
    <!-- Show a teaser: "Stay tuned for our upcoming feature: Task
    Prioritization!" -->
    {% endif %}
```
> Here is an example of our previous context processor using a cache:
```python
    from django.core.cache import cache
    def feature_flags(request):
        user = request.user
        flags = {
            "is_priority_feature_enabled": False,
        }
        # Ensure the user is authenticated before checking groups
        if user.is_authenticated:
            # Using the user's id to create a unique cache key
            cache_key = f"user_{user.id}_is_priority_feature"
            # Try to get the value from the cache
            is_priority_feature = cache.get(cache_key)
            if is_priority_feature is None: # If cache miss
                is_priority_feature = user.groups.filter(
                    name="Task Prioritization Beta Testers"
                ).exists()
            # Store the result in the cache for, say, 5 minutes (300 seconds)
            cache.set(cache_key, is_priority_feature, 300)
            flags["is_priority_feature_enabled"] = is_priority_feature
        return flags
```

- ### Debugging Django Templates
```html
    <pre>{% debug %}</pre>
```

- ### Optimizing Template Rendering
    - #### Minimize Database Queries
        - **Use select_related and prefetch_related**: When dealing with
            **ForeignKey** or **OneToOneField**, **select_related** fetches related
            objects in a single query. When dealing with reverse **ForeignKey** or
            **ManyToMany** fields, consider using **prefetch_related**. There are some
            situations where the **select_related** can lead to worse performance
            since the join query could be more expensive that query each table.
        - **Avoid using len(queryset):** Instead, use queryset.count() to get the
            number of items in a queryset without evaluating it. Note that is the
            query was already evaluated you may prefer to use len instead of count.
        - **Limit QuerySets:** If you only need a few items, use [:n] slicing. For
            example, **Article.objects.all()[:5]** only fetches five articles.
- ### Securing Django Templates
<!--the end chapter 6-->

<!--chapter 7-->
## 7. Forms in Django
- ### Understanding Django Forms
    - Here is and example fo a raw HTML form to create a new Task object without using Django forms:
    ```HTML
    <form action="/tasks/new/" method="POST">
      <label for="title">Title:</label><br>
      <input type="text" id="title" name="title" required><br>
      <label for="description">Description:</label><br>
      <textarea id="description" name="description"></textarea><br>
      <label for="status">Status:</label><br>
      <select id="status" name="status">
        <option value="UNASSIGNED">Unassigned</option>
        <option value="IN_PROGRESS">In Progress</option>
        <option value="DONE">Completed</option>
        <option value="ARCHIVED">Archived</option>
      </select><br>
      <input type="submit" value="Create Task">
    </form>
    ```
- ### Creating Your First Django Form
> Create: tasks/forms.py 
```python
    from django import forms
    from .models import Task
    class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status"]
```
- ### Rendering Forms in Templates

```shell
    poetry shell
    poetry add django-widget-tweaks
```
```HTML
{% extends "tasks/base.html" %}
{% load widget_tweaks %} 
{% block content %}
<div class="d-flex justify-content-center align-items-center vh-100">
  <div class="w-50">
    <div class="card">
      <div class="card-header">
        <h2 class="text-center">Create a New Task</h2>
      </div>
      <div class="card-body">
        <form method="post" 
        action="{% if task.pk %}{% url 'tasks:task-update' task.pk %}{% else %}{% url 'tasks:task-create' %}{% endif %}">
          {% csrf_token %} {% for field in form %}
          <div class="mb-3">
            <label for="{{ field.id_for_label }}" class="form- label"
              >{{ field.label }}</label
            >
            {% if field.errors %}
            <div class="alert alert-danger">{{ field.errors }}</div>
            {% endif %} {{ field|add_class:"form-control" }}
          </div>
          {% endfor %}
          <button type="submit" class="btn btn-primary w- 100">Save</button>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

- ### Handling Form Submission in Views

- ### Working with Form Fields

- ### File and Image Upload Field

- ### Data Validation with Django Forms

- ### Displaying Form Errors

- ### Advanced Form Handling: ModelForms and Formsets

- ### Preventing Double Submission with Forms
