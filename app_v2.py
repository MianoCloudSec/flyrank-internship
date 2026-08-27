import sqlite3
from fastapi import FastAPI

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