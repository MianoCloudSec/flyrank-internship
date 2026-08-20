from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A small in-memory CRUD API for managing a to-do list.",
    version="1.0",
)

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Walk the dog", "done": False},
    {"id": 3, "title": "Finish W2 assignment", "done": True},
]


class TaskCreate(BaseModel):
    title: str = ""


class TaskUpdate(BaseModel):
    title: str = ""
    done: bool = False


@app.get("/")
def root():
    """Describe the API and list its main resource."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health")
def health():
    """Liveness check — confirms the server is running."""
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    """Return every task currently stored in memory."""
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Return a single task by id, or 404 if it doesn't exist."""
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return task


@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    """Create a new task. Title is required and cannot be empty."""
    title = new_task.title.strip()

    if title == "":
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    next_id = max((t["id"] for t in tasks), default=0) + 1

    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)

    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    """Replace a task's title and done status. 404 if the id is unknown."""
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    title = update.title.strip()

    if title == "":
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    task["title"] = title
    task["done"] = update.done

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task by id. 404 if the id is unknown."""
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    tasks.remove(task)

    return None