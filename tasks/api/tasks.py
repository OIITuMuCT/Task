from ninja import Router

router = Router()


@router.get("/")
def list_tasks(request):
    return {
        "results": [
            {"id": 1, "title": "test title"},
        ]
    }
