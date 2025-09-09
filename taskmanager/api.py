from ninja import NinjaAPI
from django.core.exceptions import ObjectDoesNotExist
from tasks.api.tasks import router as tasks_router
from accounts.api.security import ApiTokenAuth

api_v1 = NinjaAPI(version="v1", auth=ApiTokenAuth())

api_v1.add_router('/tasks/', tasks_router)


@api_v1.exception_handler(ObjectDoesNotExist)
def on_object_does_not_exist(request, exc):
    """
    Custom exception handler for ObjectDoesNotExist.
    """
    return api_v1.create_response(request, {"message": "Object not found."}, status=404)
