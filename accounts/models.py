import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, User, PermissionsMixin


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    biography = models.TextField()
    photo = models.ImageField(upload_to="user_photos/", blank=False)


class Organization(models.Model):
    name = models.CharField(max_length=255)

class ApiToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.token)


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault("organization_id", 1)  # or another default value

#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self.create_user(username, email, password, **extra_fields)


# class TaskManagerUser(AbstractUser):
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField()

#     objects = CustomUserManager()
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []

#     class Meta:
#         unique_together = ("organization", "username", "email")

#     def has_perm(self, perm, obj=None):
#         return self.is_staff

#     def has_module_perms(self, app_label: str) -> bool:
#         return self.is_staff
