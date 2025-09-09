from ninja import NinjaAPI
from django.core.exceptions import ObjectDoesNotExist
from tasks.api.tasks import router as tasks_router

api = NinjaAPI()

api.add_router('/tasks/', tasks_router)


@api.exception_handler(ObjectDoesNotExist)
def on_object_does_not_exist(request, exc):
    """
    Custom exception handler for ObjectDoesNotExist.
    """
    return api.create_response(request, {"message": "Object not found."}, status=404)
