import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A CRUD API backed by a real SQLite database.",
    version="2.0",
)

DB_FILE = "tasks.db"


def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Buy milk", False),
                ("Walk the dog", False),
                ("Finish W2 assignment", True),
            ],
        )

    connection.commit()
    connection.close()


init_db()


class TaskCreate(BaseModel):
    title: str = ""


class TaskUpdate(BaseModel):
    title: str = ""
    done: bool = False


@app.get("/tasks")
def list_tasks():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    connection.close()

    return [
        {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
        for row in rows
    ]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    title = new_task.title.strip()

    if title == "":
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, False),
    )
    connection.commit()

    new_id = cursor.lastrowid

    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    connection.close()

    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    existing = cursor.fetchone()

    if existing is None:
        connection.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    title = update.title.strip()

    if title == "":
        connection.close()
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (title, update.done, task_id),
    )
    connection.commit()

    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    connection.close()

    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    existing = cursor.fetchone()

    if existing is None:
        connection.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()
    connection.close()

    return None