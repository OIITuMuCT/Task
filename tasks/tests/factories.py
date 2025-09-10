import factory

from accounts.models import Organization
from tasks.models import Task, TaskStatus
from django.contrib.auth import get_user_model


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    organization = factory.SubFactory(OrganizationFactory)

