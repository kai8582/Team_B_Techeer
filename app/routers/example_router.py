from fastapi import APIRouter
from app.celery_app import add

router = APIRouter()

@router.get("/add-task")
def add_task(x: int, y: int):
    task = add.delay(x, y)
    return {"task_id": task.id} 