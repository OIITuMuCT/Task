# Task Manager

- [1. Creating a **_Task_** model](#1-creating-a-task-model)
  - [Extending the models](#extending-the-models)
- [2. Django's database API: Create, retrieve, update, and delete operations](#2-djangos-database-api-create-retrieve-update-and-delete-operations)
- [3. Django's admin interface: Registering models and manipulating data](#3-djangos-admin-interface-registering-models-and-manipulating-data)
- [4. Introduction to Django's ORM: Queries and aggregations](#4-introduction-to-djangos-orm-queries-and-aggregations)

- [5. Django Views and URL Handling](#5-django-views-and-url-handling)
  - [Introduction to Django's Generic Views](#introduction-to-djangos-generic-views)
  - [Writing Your First Django View](#writing-your-first-django-view)
    - [TaskListView](#tasklistview)
    - [TaskDetailView](#taskdetailview)
    - [TaskCreateView](#taskcreateview)
    - [TaskUpdateView](#taskupdateview)
    - [TaskDeleteView](#taskdeleteview)
  - [Class-based Views Mixins](#class-based-views-mixins)
    - [Attribute Mixin](#attribute-mixin)
    - [Data Modification Mixin](#data-modification-mixin)
    - [Fetching data](#fetching-data)
    - [Redirect and Success URL Handling](#redirect-and-success-url-handling)
  - URL Configuration in DjangoCreating URL Patterns for Your Views
  - Using Django’s HttpRequest and HttpResponse Objects
  - Handling Dynamic URLs with Path Converters
  - Understanding Django’s URL Namespace and Naming URL Patterns
  - Introduction to Function-based Views
  - Using Function-based Views with a Service Layer
  - Pessimistic and Optimistic Locking Using Views and a Service Layer
  - Error Handling with Custom Error Views


## 1. Creating a **_Task_** model
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

## 2. Django's database API: Create, retrieve, update, and delete operations

## 3. Django's admin interface: Registering models and manipulating data

> ### - Firstly, you need to create an empty migration:
>
> > ### - `shell: python manage.py makemigrations tasks --empty`
>
> ### - Configure the groups from it or create a data migration
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

## 4. Introduction to Django's ORM: Queries and aggregations

> ### - Django uses the double underscore is a notation to indicate
>
> ### a separation in the query and it could be used to perform comparisons:

- **gt**: Greater than
- **gte**: Greater than or equal to
- **lte**: Less than or equal to
- **contains**: Field contains the value. Case-sensitive
- **in**: Within a range
- **isnull**: is NULL (or not)

### Extending the models
<details>  
<summary>Click to expand</summary>

> - **The One-to-One Relationship(OneToOneField):** A one-to-one relationship
>   implies that one object is related to exactly one other object. This can be
>   seen as a constrained version of the ForeignKey, where the reverse relation
>   is unique.
>
> ```python
>    from django.db import models
>    from django.contrib.auth.models import User
>
>    class Profile(models.Model):
>        user = models.OneToOneField(User, on_delete=models.CASCADE)
>        # Other fields...
> ```

> - **The One-To-Many Relationship(OneToManyField):** A One-To-Many relationship implies one object can be related to several others.
>
> ```python
>    from django.db import models
>    from django.contrib.auth.models import User
>    class Task(models.Model):
>       …
>       creator = models.ForeignKey(User,
>           related_name='created_tasks',
>           on_delete=models.CASCADE)
> ```

> - **The Many-To-Many Relationship(ManyToManyField):** In this relationship, objects can relate to
>   several others, which, in turn, can associate with multiple entities.
>
> ```python
>   class Sprint(models.Model):
>       name = models.CharField(max_length=200)
>       description = models.TextField(blank=True, null=True)
>       start_date = models.DateField()
>       end_date = models.DateField()
>       created_at = models.DateTimeField(auto_now_add=True)
>       updated_at = models.DateTimeField(auto_now=True)
>       creator = models.ForeignKey(User,
>           related_name='created_sprints', on_delete=models.CASCADE)
>       tasks = models.ManyToManyField('Task',
>           related_name='sprints', blank=True)
> ```
</details> 

## 5. Django Views and URL Handling

- [Introduction to Django's Generic Views](#introduction-to-djangos-generic-views)
- [Writing Your First Django View](#writing-your-first-django-view)
- [Class-based Views Mixins](#class-based-views-mixins)
- URL Configuration in DjangoCreating URL Patterns for Your Views
- Using Django’s HttpRequest and HttpResponse Objects
- Handling Dynamic URLs with Path Converters
- Understanding Django’s URL Namespace and Naming URL Patterns
- Introduction to Function-based Views
- Using Function-based Views with a Service Layer
- Pessimistic and Optimistic Locking Using Views and a Service Layer
- Error Handling with Custom Error Views

### Introduction to Django's Generic Views

> List and detail views:

- **ListView:** A view that displays a list of objects from a model.
- **DetailView:** A view that show a single objects and its details.
  > Date-based views:
- **ArchiveIndexView:** A date-based view that lists objects from a date-
  based queryset in the "latest firs" order
- **YearArchiveView:** A date-based view that lists objects from a year-based queryset.
- **MonthArchiveView:** A date-based view that list objects form a month-based queryset.
- **WeekArchiveView:** A date-based view that list objects from a week-based queryset.
- **DayArchiveView:** A date-based view that list objects from a day-based queryset.
- **TodayArchiveView:** A date-based view that list objects from a queryset related to the current day.
- **DateDetailView:** A date-based view that provides an object from a date-based queryset, matching the given year, month, and day.

> Editing views:

- **FormView:** A view that displays a form on GET and processes it on POST.
- **CreateView:** A view that shows a form for creating a new object, which is saved to a model.
- **UpdateView:** A view that shows a form for updating an existing objects, which is saved to a model.
- **DeleteView:** A view that shows a confirmation page and deletes an existing object.
  > The base view:
- **TemplateView:** A view that renders a specified template. This one does not involve any kind of model operations.

### Writing Your First Django View

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
### Class-based Views Mixins
#### SprintTaskWithinRangeMixin
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
<details>  
<summary>Click to expand</summary>

#### Attribute Mixin
- **ContentMixin:** Adds extra content data to the view.
- **TemplateResponseMixin:** Renders template and returns an HTTP response.
- **SingleObjectsMixin:** Provides handling to get a single object from the database.
#### Data Modification Mixin
#### Fetching data
#### Redirect and Success URL Handling

This is the content of the collapsible section. You can include any Markdown-форматированный текст, списки или код здесь.  
</details>  
