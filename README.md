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

- [8. User Authentication and Authorization in Django](#8-user-authentication-and-authorization-in-django)

  - [Understanding Django’s Authentication System](#understanding-djangos-authentication-system)
  - [Introduction to Django’s Middleware](#introduction-to-djangos-middleware)
  - [Understanding Django Middleware](#understanding-django-middleware)
  - [User Registration with Django’s User Model](#user-registration-with-djangos-user-model)
  - [Authenticating Users: Login and Logout](#authenticating-users-login-and-logout)
  - [Managing User Sessions](#managing-user-sessions)
  - [Password Management in Django: Hashing and Password Reset](#password-management-in-django-hashing-and-password-reset)
  - [User Authorization: Permissions and GroupsProtecting Views with Login Required Decorators](#user-authorization-permissions-and-groupsprotecting-views-with-login-required-decorators)
  - [Multi-tenant authentication with Custom Django’s User Model](#multi-tenant-authentication-with-custom-djangos-user-model)
  - [Security Best Practices in Django](#security-best-practices-in-django)

- [9. Django Ninja and APIs](#9-django-ninja-and-apis)
  - [Introduction to API design](#introduction-to-api-design)
  - [API Design-first approach](#api-design-first-approach)
  - [HTTP Response status codesIntroduction to Django Ninja](#http-response-status-codesintroduction-to-django-ninja)
  - [Setting Up Django Ninja in Your Project](#setting-up-django-ninja-in-your-project)
  - [Building Your First API with Django Ninja](#building-your-first-api-with-django-ninja)
  - [Request and Response Models with Pydantic](#request-and-response-models-with-pydantic)
  - [API Documentation](#api-design-first-approach)
  - [Understanding HTTP Methods in Django Ninja](#understanding-http-methods-in-django-ninja)
  - [API Pagination](#api-pagination)
  - [Working with Path Parameters and Query Parameters](#working-with-path-parameters-and-query-parameters)
  - [Validation and Error Handling in Django Ninja](#validation-and-error-handling-in-django-ninja)
  - [Authenticating API Users](#authenticating-api-users)
  - [Securing APIs: Permissions and Throttling](#securing-apis-permissions-and-throttling)
  - [Versioning Your API](#versioning-your-api)

## 1. Creating a **_Task_** model

  <details>  
    <summary style="margin-left: 20px">Click to expand</summary>

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

## 3. Django's admin interface: Registering models and manipulating data

<!--Chapter 3-->

- #### Firstly, you need to create an empty migration:

  ```shell
    python manage.py makemigrations tasks --empty
  ```

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

  <details>
    <summary>Click to expand</summary>

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

  </details>

- ### Handling Form Submission in Views

  <details>
  <summary>Click to expand</summary>

  ```python
    # tasks/forms.py
    from django import forms

    class ContactForm(forms.ModelForm):
        form_email = forms.EmailField(required=True)
        subject = forms.CharField(required=True)
        message = forms.CharField(widget=forms.Textarea, required=True)
  ```

  ```python
    # tasks/views.py
    from django.views.generic import FormView
    from django.urls import reverse_lazy
    from tasks.forms import ContactForm
    from tasks import services

    class ContactFormView(FormView):
        template_name = "tasks/contact_form.html"
        form_class = ContactForm
        success_url = reverse_lazy("tasks:contact-success")

        def form_valid(self, form):
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            from_email = form.cleaned_data.get("from_email")
            services.send_contact_email(subject, message, from_email,
            ["your-email@example.com"])
            return super().form_valid(form)
  ```

  ```HTML
  <!--tasks/contact_form.html-->
  {% extends "tasks/base.html" %}
  {% load widget_tweaks %}

  {% block content %}
  <div class="d-flex justify-content-center align-items-center vh-100">
      <div class="w-50">
          <div class="card">
              <div class="card-header">
                  <h2 class="text-center">Contact Us!</h2>
              </div>
              <div class="card-body">
                  <form action="{% url "tasks:contact" %}" method="post">
                      {% csrf_token %}
                      {% for field in form %}
                      <div class="mb-3">
                          <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                          {% if field.errors %}
                          <div class="alert alert-danger">
                              {{ field.errors }}
                          </div>
                          {% endif %}
                          {{ field|add_class:"form-control"}}
                      </div>
                      {% endfor %}
                      <button type="submit" class="btn btn-primary w-100">Send</button>
                  </form>
              </div>
          </div>
      </div>
  </div>
  {% endblock %}
  ```

  ```HTML
  <!-- tasks/contact_success.html -->
    {% extends "base.html" %}
    {% block content %}
      <div class="container">
        <h1>Contact Message Sent!</h1>
        <p>Thank you for reaching out! We have received your message and will respond as soon as possible.</p>
        <a href="{% url 'home' %}">Return Home</a>
      </div>
    {% endblock %}
  ```

  ```python
    #  send to email
    from django.shortcuts import render, redirect, reverse
    from .forms import ContactForm
    from .services import send_contact_email
    def contact_form_view(request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data.get('subject')
                message = form.cleaned_data.get('message')
                from_email = form.cleaned_data.get('from_email')
            send_contact_email(subject, message, from_email, 'your-email@example.com')
            return redirect(reverse('contact-success'))
        else:
            form = ContactForm()
        return render(request, 'contact_form.html', {'form': form})
  ```

  </details>

- ### Working with Form Fields

  ```HTML
    {{ form.as_div }} Input elements will be wrapped between divs.
    {{ form.as_table }} Fields will be rendered to a table
    {{ form.as_p }} Input elements will be wrapped between p tags.
    {{ form.as_ul }} Inputs will be rendered using the HTML unordered list.
  ```

  - Custom form fields

    - **to_python(self, value):** This method converts the value into the
      correct Python datatype. For example, if you have a custom field that
      deals with numeric data, you would use this method to ensure that the
      data is converted into a Python integer or float.
    - **validate(self, value):** This method runs field-specific validation
      rules. You could raise the **ValidationError** from here if the validation
      fails.
    - **clean(self, value):** This method is used to provide the **cleaned**
      data, which is the result of calling **to_python()** and **validate()**. You
      usually don’t need to override this unless you need to change its
      behavior fundamentally.
    - **bound_data(self, data, initial):** This returns the value that
      should be shown for this field when rendering it with the specified
      initial data and the submitted data. This method is typically used for
      fields where the user’s input is not necessarily the same as the output.
    - **prepare_value(self, value):** Converts Python objects to query
      string values.
    - **widget_attrs(self, widget):** This adds any HTML attributes needed
      for your widget based on the field.

    ```python
    from typing import Any
    from django import forms
    from django.core.validators import EmailValidator

    email_validator = EmailValidator(message="One or more email addresses are not valid")

    class EmailsListField(forms.CharField):
        def to_python(self, value):
            "Normalize data to a list of strings."
            # Return an empty list fi no input was given.
            if not value:
                return []
            return [email.strip() for email in value.split(',')]
        def validate(self, value: Any) -> None:
            "Check if value consists only of valid emails."
            super().validate(value)
            for email in value:
                email_validator(email)
    ```

    ```python
    # tasks/models.py and add the new model:
    class SubscribedEmail(models.Model):
        email = models.EmailField()
        task = models.ForeignKey(Task, on_delete=models.CASCADE,
        related_name="watchers")
    ```

    ```python
    from django import forms
    from tasks.fields import EmailsListField
    from .models import SubscribedEmail, Task
    class TaskForm(forms.ModelForm):
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
            for email_str in self.cleaned_data["watchers"]:
                SubscribedEmail.objects.create(email=email_str, task=task)
            return task
    ```

    ```html
    <!-- Update templates/tasks/task_detail.html -->
    {% extends "tasks/base.html" %}

    {% block content %}
    <div class="vh-100 d-flex justify-content-center align-items-center">
      <div class="container text-center">
        <h1 class="mb-4">{{ task.title }}</h1>
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">Description</h2>
            <p class="card-text">{{ task.description }}</p>
            <!--Emails List-->
            <h3>Watchers</h3>
            <ul class="list-unstyled">
              {% for watcher in task.watchers.all %}
              <li>{{ watcher.email }}</li>
              {% endfor %}
            </ul>
          </div>
        </div>
        <div class="mt-4 d-inline-block">
          <a href="{% url "tasks:task-update" task.id %}" class="btn btn-primary me-2">Edit</a>
          <a href="{% url "tasks:task-delete" task.id %}" class="btn btn-danger">Delete</a>
          <a href="{% url "tasks:task-list" %}" class="btn btn-secondary">Back to List</a>
        </div>
      </div>
    </div>
    {% endblock %}
    ```

- ### File and Image Upload Field

  ```python
  class Task(models.Model):
      …
      file_upload = models.FileField(upload_to="tasks/files/",
      null=True, blank=True)
      image_upload = models.ImageField(upload_to="tasks/images/",
      null=True, blank=True)
  ```

  ```shell
  poetry add Pillow
  poetry shell
  python manage.py makemigrations
  python manage.py migrate
  ```

  ```python
  MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
  MEDIA_URL = "/media/"


  class TaskForm(forms.ModelForm):
      …
      class Meta:
          model = Task
          fields = [
              "title", "description", "status",
              "watchers", "file_upload", "image_upload"
          ]
  ```

  ```python
  # taskmanager/urls.py
  from django.conf import settings
  from django.conf.urls.static import static
  urlpatterns = [
      …
  ]
  if settings.DEBUG:
      urlpatterns += static(settings.MEDIA_URL,
      document_root=settings.MEDIA_ROOT)
  ```

  ```html
  <!-- # templates/tasks/task_details.html -->
  {% if task.file_upload %}
  <a href="{{ task.file_upload.url }}" download>Download File</a>
  {% endif %} {% if task.image_upload %}
  <div>
    <img
      src="{{ task.image_upload.url }}"
      alt="Task Image"
      style="max-width: 300px;"
    />
  </div>
  {% endif %}
  ```

- ### Data Validation with Django Forms

  ```python
  from django import forms
  from django.core.validators import (
      MaxValueValidator,
      EmailValidator,         # Validates that a value is a valid email address.
      URLValidator,           # Validates that a value is a valid URL.
      RegexValidator,         # Validates a value based on a provided regular expression
      MinLengthValidator,     # Validates that a value doesn’t exceed a certain length.
      MinValueValidator,      # Validates that a value is at least a specified minimum.
      MaxValueValidator,      # Validates that a value doesn’t exceed a specified maximum.
      FileExtensionValidator, # Validates that a file has a specific extension.
  )

  class TaskForm(forms.Form):
      priority = forms.IntegerField(validators=[MaxValueValidator(100)])
  ```

  - Clean methods

  ```python
      def clean_email(self) -> str:
          email = self.cleaned_data.get("email")
          email = email.strip()
          validate_email(email)
          return email

      def clean(self) -> dict:
        cleaned_data = super().clean()
        # perform validations or cleanups
        return cleaned_data
  ```

  - ModelForm Validation
    - max_length=100,

- ### Displaying Form Errors
  ```html
  <form method="post">
    {% csrf_token %} {% for field in form %}
    <div class="form-group mb-3">
      <label for="{{ field.id_for_label }}" class="form-label"
        >{{ field.label }}</label
      >
      {{ field|add_class:"form-control" }} {% if field.errors %}
      <div class="alert alert-danger mt-2">
        {% for error in field.errors %}
        <p class="mb-0"><strong>{{ error }}</strong></p>
        {% endfor %}
      </div>
      {% endif %}
    </div>
    {% endfor %} {% if form.non_field_errors %}
    <div class="alert alert-danger">
      <ul>
        {% for error in form.non_field_errors %}
        <li>{{ error }}</li>
        {% endfor %}
      </ul>
    </div>
    {% endif %}
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
  ```
- ### Advanced Form Handling: ModelForms and Formsets

- ### Preventing Double Submission with Forms

## 8. User Authentication and Authorization in Django

- [Understanding Django’s Authentication System](#understanding-djangos-authentication-system)
- [Introduction to Django’s Middleware](#introduction-to-djangos-middleware)
- [Understanding Django Middleware](#understanding-django-middleware)
- [User Registration with Django’s User Model](#user-registration-with-djangos-user-model)
- [Authenticating Users: Login and Logout](#authenticating-users-login-and-logout)
- [Managing User Sessions](#managing-user-sessions)
- [Password Management in Django: Hashing and Password Reset](#password-management-in-django-hashing-and-password-reset)
- [User Authorization: Permissions and GroupsProtecting Views with Login Required Decorators](#user-authorization-permissions-and-groupsprotecting-views-with-login-required-decorators)
- [Multi-tenant authentication with Custom Django’s User Model](#multi-tenant-authentication-with-custom-djangos-user-model)
- [Security Best Practices in Django](#security-best-practices-in-django)

- ### Understanding Django’s Authentication System

  ```python
     import time
     import logginglogger = logging.getLogger(__name__)
     class RequestTimeMiddleware:
         def __init__(self, get_response):
             self.get_response = get_response

         def __call__(self, request):
             # Start the timer when a request is received
             start_time = time.time()
             # Process the request and get the response
             response = self.get_response(request)
             # Calculate the time taken to process the request
             duration = time.time() - start_time
             # Log the time taken
             logger.info(f"Request to {request.path} took {duration:.2f}
             seconds.")
             return response
  ```

- ### Introduction to Django’s Middleware
- ### Understanding Django Middleware

  ```python
    import logging
    import time

    logger = logging.getLogger(__name__)


    class RequestTimeMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            # Start the timer when a request is received
            start_time = time.time()

            # Process the request and get the response
            response = self.get_response(request)

            # Calculate the time taken to process the request
            duration = time.time() - start_time

            # Log the time taken
            logger.info(f"Request to {request.path} took {duration:.2f} seconds.")

            return response
  ```

- ### User Registration with Django’s User Model

  1. Open the project **settings.py** and add newly created application to the **INSTALLED_APPS**.
  2. Create registration view in the **accounts/views.py**
     ```python
       from django.shortcuts import render, redirect
       from django.contrib.auth.forms import UserCreationForm
       from django.contrib import messages
       def register(request):
           if request.method == "POST":
               form = UserCreationForm(request.POST)
               if form.is_valid():
                   form.save()
                   username = form.cleaned_data.get("username")
                   messages.success(request, f"Account created for {username}!")
                   return redirect("login") # Redirect to the login page or any other page you want
           else:
               form = UserCreationForm()
           return render(request, "accounts/register.html", {"form": form})
     ```
  3. Create the **templates/accounts/register.html**

     ```html
     {% extends "tasks/base.html" %} {% block content %}
     <div class="container">
       <div class="row justify-content-center">
         <div class="col-md-6">
           <h2 class="mb-4">Register</h2>
           <form action="" method="post" class="border p-4 rounded">
             {% csrf_token %} {% for field in form %}
             <div class="mb-3">
               <label for="{{field.id_for_label}}" class="form-label"
                 >{{ field.label }}</label
               >
               {{ field }} {% if field.help_text %}
               <small class="form-text text-muted">{{ field.help_text }}</small>
               {% endif %} {% for error in field.errors %}
               <div class="text-danger">{{ error }}</div>
               {% endfor %}
             </div>
             {% endfor %}
             <button type="submit" class="btn btn-primary">Register</button>
           </form>
         </div>
       </div>
     </div>
     {% endblock %}
     ```

  4. Need to set up URLs, open **accounts/urls.py**

     ```python
       from django.urls import path
       from . import views

       app_name = "accounts"

       urlpatterns = [
           path("register/", views.register, name="register"),
       ]
     ```

  5. Open the project **taskmanager/urls.py** and add the accounts URLs.

     ```python
       from django.contrib import admin
       from django.urls import include, path

       urlpatterns = [
           path("admin/", admin.site.urls),
           path("accounts/", include("accounts.urls")),
           path("", include("tasks.urls")),
       ]
     ```

  6. Navigate to http://localhost:8000/accounts/register/ and you should see the registration form.

- ### Authenticating Users: Login and Logout

  1. Open the **accounts/urls.py** and add two new paths

     ```python
       from django.urls import path
       from django.contrib.auth.views import LoginView, LogoutView
       from . import views

       urlpatterns = [
           path("register/", views.register, name="register"),
           # Add the following line
           path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login")
           path("logout/", LogoutView.as_view(), name="logout"),
       ]
     ```

  2. Create a new file in **templates/accounts/login.html**

     ```html
     {% extends 'tasks/base.html' %} {% load static %} {% block content %}
     <div class="container">
       <div class="row justify-content-center">
         <div class="col-md-6">
           <div class="card mt-5">
             <div class="card-body">
               <h2 class="text-center">Login</h2>
               <form method="post" class="mt-3">
                 {% csrf_token %}
                 <div class="mb-3">
                   <label
                     for="{{ form.username.id_for_label }}"
                     class="form-label"
                     >Username</label
                   >
                   <input
                     type="text"
                     class="form-control"
                     id="{{ form.username.id_for_label }}"
                     name="{{ form.username.name}}"
                   />
                 </div>
                 <div class="mb-3">
                   <label
                     for="{{ form.password.id_for_label }}"
                     class="form-label"
                     >Password</label
                   >
                   <input
                     type="password"
                     class="form-control"
                     id="{{ form.password.id_for_label }}"
                     name="{{ form.password.name}}"
                   />
                 </div>
                 <div class="d-grid gap-2">
                   <button type="submit" class="btn btn-primary">Login</button>
                 </div>
               </form>
             </div>
           </div>
         </div>
       </div>
     </div>
     {% endblock %}
     ```

  3. The logout view we added in the **urlpatterns** will redirect the user to a URL

     ```python
       # taskmanager/settings.py

       LOGIN_REDIRECT_URL = "tasks:task-home"
       LOGOUT_REDIRECT_URL = "accounts:login"
     ```

  4. Open the **templates/tasks/\_header.html** and update it with the new authentication links
     ```html
     <!-- Login/Logout links -->
     {% if user.is_authenticated %}
     <a
       href="{% url 'accounts:logout' %}"
       class="btn btn-danger ml-2"
       role="button"
       >Logout</a
     >
     {% else %}
     <a
       href="{% url 'accounts:login' %}"
       class="btn btn-info ml-2"
       role="button"
       >Login</a
     >
     {% endif %}
     ```

- ### Managing User Sessions
- ### Password Management in Django: Hashing and Password Reset

  1. Open the **accounts/urls.py** and add the new paths:
     <details>
     <summary>Click to expand</summary>

     ```python
       from django.urls import path, reverse_lazy
       from django.contrib.auth.views import (
           LoginView,
           LogoutView,
           PasswordChangeView,
           PasswordChangeDoneView,
           PasswordResetView,
           PasswordResetDoneView,
           PasswordResetConfirmView,
           PasswordResetCompleteView,
       )
       from . import views
       from tasks.views import TaskListView

       app_name = "accounts"

       urlpatterns = [
           path("register/", views.register, name="register"),
           path("profile/", TaskListView.as_view(), name="profile"),
           path(
               "login/", LoginView.as_view(template_name="accounts/login.html"), name="login"
           ),
           path("logout/", LogoutView.as_view(), name="logout"),
           path(
               "password_change/",
               PasswordChangeView.as_view(
                   success_url=reverse_lazy("accounts:password_change_done"),
                   template_name="accounts/password_change_form.html",
               ),
               name="password_change",
           ),
           path(
               "password_change/done/",
               PasswordChangeDoneView.as_view(
                   template_name="accounts/password_change_done.html"
               ),
               name="password_change_done",
           ),
           path(
               "password_reset/",
               PasswordResetView.as_view(
                   email_template_name="accounts/custom_password_reset_email.html"
               ),
               name="password_reset",
           ),
           path(
               "password_reset/done/",
               PasswordResetDoneView.as_view(),
               name="password_reset_done",
           ),
           path(
               "password_reset/<uidb64>/<token>/",
               PasswordResetConfirmView.as_view(),
               name="password_reset_confirm",
           ),
           path(
               "reset/done/",
               PasswordResetCompleteView.as_view(),
               name="password_reset_complete",
           ),
       ]
     ```

     </details>

  2. Add in **templates/accounts/password_change.html**
     <details>
      <summary>Click to expand</summary>
      
     ```html
     {% extends "tasks/base.html" %} {% load widget_tweaks %} {% block content%}
     <div class="container my-5">
       <div class="row">
         <div class="col-lg-6 offset-lg-3">
           <div class="card">
             <div class="card-body">
               <h2 class="card-title">Change Password</h2>
               <form method="post" class="mt-4">
                 {% csrf_token %}
                 <div class="mb-3">
                   <!-- Assuming you have fields like 'old_password',
                     'new_password', 'confirm_new_password' in your form -->
                   <label
                     for="{{ form.old_password.id_for_label }}"
                     class="form-label"
                     >Old Password</label
                   >
                   {{ form.old_password|add_class:"form-control" }}
                 </div>
                 <div class="mb-3">
                   <label
                     for="{{ form.new_password.id_for_label }}"
                     class="form-label"
                     >New Password</label
                   >
                   {{ form.new_password1|add_class:"form-control" }}
                 </div>
                 <div class="mb-3">
                   <label
                     for="{{ form.confirm_new_password.id_for_label }}"
                     class="form-label"
                     >Confirm New Password</label
                   >
                   {{ form.new_password2|add_class:"form-control" }}
                 </div>
                 <button type="submit" class="btn btn-primary">
                   Change Password
                 </button>
               </form>
             </div>
           </div>
         </div>
       </div>
     </div>
     ```

     </details>

  3. Add in **templates/accounts/password_change_done.html**
     <details>
      <summary>Click to expand</summary>

     ```html
     {% extends "tasks/base.html" %} {% block content %}
     <div class="container my-5">
       <div class="row">
         <div class="col-lg-6 offset-lg-3">
           <div class="card">
             <div class="card-body text-center">
               <h2 class="card-title">Password Change Successful</h2>
               <p class="card-text">
                 Your password has been changed successfully!
               </p>
               <a href="{% url 'accounts:login' %}" class="btn btn-primary"
                 >Login Again</a
               >
             </div>
           </div>
         </div>
       </div>
     </div>
     {% endblock %}
     ```

     </details>

  4. Create a new file in **templates/accounts/password_reset_form.html**
      <details>
      <summary>Click to expand</summary>

     ```html
     {% extends "tasks/base.html" %} {% block content %}
     <div class="container mt-5">
       <div class="row justify-content-center">
         <div class="col-md-6">
           <div class="card">
             <div class="card-header bg-primary text-white">
               <h2>Reset Password</h2>
             </div>
             <div class="card-body">
               <form method="post">
                 {% csrf_token %}
                 <div class="mb-3">
                   {{ form.email.label_tag }} {{ form.email }} {% if
                   form.email.errors %}
                   <div class="alert alert-danger mt-2">
                     {{ form.email.errors }}
                   </div>
                   {% endif %}
                 </div>
                 <button type="submit" class="btn btn-primary">
                   Reset Password
                 </button>
               </form>
             </div>
           </div>
         </div>
       </div>
     </div>
     {% endblock %}
     ```

     </details>

  5. Create a new file in **templates/accounts/custom_password_reset_email.html**
     ```html
     {% autoescape off %} Hi {{ user.username }}, You're receiving this email
     because you requested a password reset for your account. Please go to the
     following page and choose a new password: {{ protocol }}://{{ domain }}{%
     'accounts:password_reset_confirm' uidb64=uid token=token %} url Thanks for
     using our site! {% endautoescape %}
     ```
  6. create a new file in **accounts/templates/password_reset_confirm_form.html**
     <details>
      <summary>Click to expand</summary>

     ```html
     {% extends "tasks/base.html" %} {% block content %}
     <div class="container mt-5">
       <div class="row justify-content-center">
         <div class="col-md-6">
           <div class="card">
             <div class="card-header bg-primary text-white">
               <h3>Set New Password</h3>
             </div>
             <div class="card-body">
               <form method="post">
                 {% csrf_token %}
                 <div class="mb-3">
                   {{ form.new_password1.label_tag }} {{ form.new_password1 }}{%
                   if form.new_password1.errors %}
                   <div class="alert alert-danger mt-2">
                     {{ form.new_password1.errors }}
                   </div>
                   {% endif %}
                 </div>
                 <div class="mb-3">
                   {{ form.new_password2.label_tag }} {{ form.new_password2 }}
                   {% if form.new_password2.errors %}
                   <div class="alert alert-danger mt-2">
                     {{ form.new_password2.errors }}
                   </div>
                   {% endif %}
                 </div>
                 <button type="submit" class="btn btn-primary">
                   Change Password
                 </button>
               </form>
             </div>
           </div>
         </div>
       </div>
     </div>
     {% endblock %}
     ```

     </details>

  7. Create a new file in **templates/accounts/password_reset_complete.html**
     <details>
      <summary>Click to expand</summary>

     ```html
     {% extends "base.html" %} {% load static %} {% block content %}
     <div class="container mt-5">
       <div class="row justify-content-center">
         <div class="col-md-6">
           <div class="card">
             <div class="card-body text-center">
               <h2 class="card-title">Password Reset Successful</h2>
               <p class="card-text">
                 Your password has been reset successfully. You can now log in
                 using your new password.
               </p>
               <a
                 href="{% url 'accounts:login' %}"
                 class="btn btn-primary mt-
          3"
                 >Login</a
               >
             </div>
           </div>
         </div>
       </div>
     </div>
     {% endblock %}
     ```

     </details>

- ### User Authorization: Permissions and GroupsProtecting Views with Login Required Decorators

  1. Add a **@login_required** decorator to our create task on sprint view

     ```python
       from django.contrib.auth.decorators import login_required

       @login_required  # Add decorator
       def create_task_on_sprint(request: HttpRequest, sprint_id: int) -> HttpResponseRedirect:
           if request.method == "POST":
           task_data: Dict[str, str] = {
              'title': request.POST.get("title", "Untitled"),
              'description': request.POST.get("description", ""),
              'status': request.POST.get("status", "UNASSIGNED"),
           }
           task = create_task_and_add_to_sprint(task_data, sprint_id, request.user)
          return redirect("task-detail", task_id=task.id)
     ```

  2. The simplest way to authenticate the views is to inherit from the **LoginRequiredMixin**:

     ```python
     from django.contrib.auth.mixins import LoginRequiredMixin
     from django.views.generic import ListView

     class TaskListView(LoginRequiredMixin, ListView):
         model = Task
         template_name = 'task_list.html'
         context_object_name = 'tasks'
     ```

  3. There is an alternative way using the **login_required** decorator:

     ```python
         from django.utils.decorators import method_decorator
         from django.contrib.auth.decorators import login_required
         from django.views.generic import ListView

         @method_decorator(login_required, name='dispatch')
         class TaskListView(ListView):
             model = Task
             template_name = 'task_list.html'
             context_object_name = 'tasks'
     ```

- ### Multi-tenant authentication with Custom Django’s User Model
- ### Security Best Practices in Django

## 9. Django Ninja and APIs

- ### Introduction to API design
- ### API Design-first approach
- ### HTTP Response status codesIntroduction to Django Ninja
- ### Setting Up Django Ninja in Your Project
- ### Building Your First API with Django Ninja
- ### Request and Response Models with Pydantic
- ### API Documentation
- ### Understanding HTTP Methods in Django Ninja

  Open the file and add the new endpoint **tasks/api/tasks.py**

  ```python
      from http import HTTPStatus
      from django.http import HttpRequest, HttpResponse

      from ninja import Router

      router = Router()

      # Create
      @router.post("/", response={201: CreateSchemaOut})
      def create_task(request: HttpResponse, task_in: TaskSchemaIn):
        creator = request.user
        return service.create_task(creator, **task_in.dict())

      # Read(list)
      @router.get("/", response=list[TaskSchemaOut])
      def list_task(request):
          return service.list_tasks()

      # Read(object)
      @router.get("/{int:task_id}", response=TaskSchemaOut)
      def get_task(request: HttpRequest, task_id: int):
        task = service.get_task(task_id)
        if task is None:
            raise Http404("Task not found.")
        return task

      # Update
      @router.put("/{int:task_id}")
      def update_task(request: HttpResponse, task_id: int, task_data:TaskSchemaIn):
        service.update_task(task_id=task_id, task_data=task_data.dict())
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

      # Delete
      @router.delete("/{int:task_id}")
      def delete_task(request: HttpRequest, task_id: int):
        service.delete_task(task_id=task_id)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
  ```

- ### API Pagination

  ```python
    from ninja import Schema

    class TaskManagerPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        skip_records: int
    class Output(Schema):
        items: list[Any]
        count: int
        page_size: int
    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip_records = pagination.skip_records
        return {
            "data": queryset[skip_records: skip_records + 5],
            "count": queryset.count(),
            "page_size": 5,
        }
  ```

  Adding in **taskmanager/settings.py**

  ```shell
    NINJA_PAGINATION_CLASS=TaskManagerPagination
  ```

- ### Working with Path Parameters and Query Parameters
- ### Validation and Error Handling in Django Ninja
- ### Authenticating API Users

  Token-Based Authentication

  ```python
    # accounts/models.py
    import uuid
    from django.db import models

    class ApiToken(models.Model):
        token = models.UUIDField(default=uuid.uuid4, unique=True)
        user = models.ForeignKey(TaskManagerUser, on_delete=models.CASCADE)

        def __str__(self):
          return str(self.token)
  ```

  Creating a new file **tasks/api/security.py**

  ```python
    from account.api.security import ApiTokenAuth

    @router.get("/", response=list[TaskSchemaOut], auth=ApiTokenAuth())
    @paginate
    def list_tasks(request):
      return service.list_tasks()
  ```

  Open the file **taskmanager/api.py** and modify it to integrate the new authentication method

  ```python
    from accounts.api.security import ApiTokenAuth
    api_v1 = NinjaAPI(version="v1", auth= ApiTokenAuth ())

    #If we don’t want to affect the project globally, we can add
    # authentication at the router level:

    from accounts.api.security import ApiTokenAuth
    router = Router(auth= ApiTokenAuth ())
  ```

  Create a new file for the service layer **accounts/service.py** and populate it with the following contents:

  ```python
      # accounts/service.py
      from accounts.models import ApiToken
      def generate_token(user: AbstractUser) -> str:
          token, _ = ApiToken.objects.get_or_create(user=user)
          return str(token.token)
  ```

  Let's now create a view to display the token to the user:

  ```python
    from django.contrib.auth.decorator import login_required
    from django.shortcuts import redirect, render
    from accounts.service import generate_token

    @login_required
    def token_generation_view(request):
        token = generate_token(request.user)
        return render(request, "accounts/token_display.html", {"token": token})
  ```

  Then we need to add the new view to the **accounts/urls.py**:

  ```python
    urlpatterns = [
        # ...
        path("show-api-token/", views.token_generation_view, name="api-token"),
    ]
  ```

  We still need to create the new template to display the token in the **templates/accounts/token_display.html:**

  ```html
  {% extends 'tasks/base.html' %} {% load static %} {% block content %}
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta
        name="viewport"
        content="width=device-width, initial-
          scale=1.0"
      />
      <title>API Token</title>
    </head>
    <body class="bg-light">
      <div class="container py-5">
        <div class="row justify-content-center">
          <div class="col-md-8">
            <div class="card">
              <div class="card-header">
                <h1 class="card-title">Your API Token</h1>
              </div>
              <div class="card-body">
                {% if token %}
                <p class="card-text">Your token: <code>{{ token }} </code></p>
                {% else %}
                <p class="card-text">No token available.</p>
                {% endif %}
              </div>
            </div>
          </div>
        </div>
      </div>
    </body>
  </html>
  {% endblock %}
  ```

  ```shell
    ❯ curl http://localhost:8000/api/v1/tasks/archive/2025/09/08
    {"detail": "Unauthorized"}

    ❯ curl -H "Authorization: Bearer 74d98426-d7b9-43d6-91d2-2e21c46a1db9" \
      http://localhost:8000/api/v1/tasks/archive/2025/09/08

    {"items": [
          {
            "title": "New Task with uuid field",
            "description": "dsdfsfs"
          },
          {
            "title": "New Task from udid",
            "description": "Good a Create new tasks uuid"
          },
          {
            "title": "Enhanced Satellite Data Analisis",
            "description": "Develop a comprehensive analytical model to process"
          }
      ], "count": 3}
  ```

JSON Web Tokens Authentication

- ### Securing APIs: Permissions and Throttling
- ### Versioning Your API
