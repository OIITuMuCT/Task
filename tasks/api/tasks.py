from ninja import Router
from ninja.pagination import paginate
from django.http import Http404
from http import HTTPStatus
from tasks.schemas import CreateSchemaOut, TaskSchemaIn, TaskSchemaOut
from django.http import HttpRequest, HttpResponse

from tasks import services

router = Router(tags=["tasks"])


@router.post("/", response={201: CreateSchemaOut})
def create_task(request: HttpRequest, task_in: TaskSchemaIn):
    creator = request.user
    return services.create_task(creator, **task_in.dict())


@router.get("/", response=list[TaskSchemaOut])
@paginate
def list_tasks(request):
    return services.list_tasks()


@router.get("/{int:task_id}", response=TaskSchemaOut)
def get_task(request: HttpRequest, task_id: int):
    task = services.get_task(task_id)
    if task is None:
        raise Http404("Task not found.")
    return task


@router.put("/{int:task_id}")
def update_task(request: HttpRequest, task_id: int, task_data: TaskSchemaIn):
    services.update_task(task_id=task_id, task_data=task_data.dict())
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


@router.delete("/{int:task_id}")
def delete_task(request: HttpRequest, task_id: int):
    services.delete_task(task_id=task_id)
    return HttpResponse(status=HTTPStatus.NO_CONTENT)
