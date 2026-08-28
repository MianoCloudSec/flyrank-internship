from fastapi import FastAPI, HTTPException

from app_v3.models import TaskCreate, TaskUpdate
from app_v3.repositories.postgres_repository import PostgresTaskRepository
from app_v3.service import TaskService

app = FastAPI(
    title="Task API",
    description="Layered CRUD API — routes, service, repository.",
    version="3.0",
)

repository = PostgresTaskRepository()
service = TaskService(repository)


@app.get("/tasks")
def list_tasks():
    return service.list_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    task, error = service.create_task(new_task.title)
    if error is not None:
        raise HTTPException(status_code=400, detail=error)
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    task, error = service.update_task(task_id, update.title, update.done)
    if error == "not_found":
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if error is not None:
        raise HTTPException(status_code=400, detail=error)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return None