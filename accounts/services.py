from django.contrib.auth.models import AbstractUser
from django.conf import settings
from accounts.models import ApiToken


def generate_token(user: AbstractUser) -> str:
    """
    Retrieves or generates a unique API token for a given user.

    If an API token already exists for the specified user, that token is returned.
    If no token exists, a new token is created and returned.

    Parameters:
    user (AbstractUser): The user instance for whom the token is to be retrieved or generated.

    Returns:
    str: The API token associated with the user.
    """
    token, _ = ApiToken.objects.get_or_create(user=user)
    return str(token.token)