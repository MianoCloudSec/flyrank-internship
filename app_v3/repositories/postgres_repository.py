import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from app_v3.models import Task
from app_v3.repositories.base import TaskRepository

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]


class PostgresTaskRepository(TaskRepository):
    def _get_connection(self):
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

    def get_all(self) -> list[Task]:
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, done FROM tasks ORDER BY id")
        rows = cursor.fetchall()
        connection.close()
        return [Task(**row) for row in rows]

    def get_by_id(self, task_id: int) -> Task | None:
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
        row = cursor.fetchone()
        connection.close()
        if row is None:
            return None
        return Task(**row)

    def create(self, title: str) -> Task:
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done",
            (title, False),
        )
        row = cursor.fetchone()
        connection.commit()
        connection.close()
        return Task(**row)

    def update(self, task_id: int, title: str, done: bool) -> Task | None:
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done",
            (title, done, task_id),
        )
        row = cursor.fetchone()
        connection.commit()
        connection.close()
        if row is None:
            return None
        return Task(**row)

    def delete(self, task_id: int) -> bool:
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        deleted_count = cursor.rowcount
        connection.commit()
        connection.close()
        return deleted_count > 0