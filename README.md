# Task Manager
## 1. Creating a ***Task*** model
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
## 2. Django's database API: Create, retrieve, update, and delete operations
## 3. Django's admin interface: Registering models and manipulating data
> ### - Firstly, you need to create an empty migration:
>> ### - ```shell: python manage.py makemigrations tasks --empty```
> ### - Configure the groups from it or create a data migration
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
## 4. Introduction to Django's ORM: Queries and aggregations
> ### - Django uses the double underscore is a notation to indicate 
> ###  a separation in the query and it could be used to perform comparisons:
- **gt**: Greater than
- **gte**: Greater than or equal to
- **lte**: Less than or equal to
- **contains**: Field contains the value. Case-sensitive
- **in**: Within a range
- **isnull**: is NULL (or not)

### Extending the models

> - **The One-to-One Relationship(OneToOneField):** A one-to-one relationship
>implies that one object is related to exactly one other object. This can be
>seen as a constrained version of the ForeignKey, where the reverse relation
>is unique.
> ```python 
>    from django.db import models
>    from django.contrib.auth.models import User
>
>    class Profile(models.Model):
>        user = models.OneToOneField(User, on_delete=models.CASCADE)
>        # Other fields...
>```