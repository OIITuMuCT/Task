from typing import Any
from ninja.security import HttpBearer
from django.http import HttpRequest
from accounts.models import ApiToken


class ApiTokenAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        if ApiToken.objects.filter(token=token).exists():
            return token
        else:
            return None
