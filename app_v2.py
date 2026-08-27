import sqlite3
from fastapi import FastAPI, HTTPException

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
    return dict(row)