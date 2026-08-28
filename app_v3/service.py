from app_v3.models import Task
from app_v3.repositories.base import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        return self.repository.get_all()

    def get_task(self, task_id: int) -> Task | None:
        return self.repository.get_by_id(task_id)

    def create_task(self, title: str) -> tuple[Task | None, str | None]:
        title = title.strip()
        if title == "":
            return None, "title is required and cannot be empty"
        task = self.repository.create(title)
        return task, None

    def update_task(self, task_id: int, title: str, done: bool) -> tuple[Task | None, str | None]:
        existing = self.repository.get_by_id(task_id)
        if existing is None:
            return None, "not_found"

        title = title.strip()
        if title == "":
            return None, "title is required and cannot be empty"

        task = self.repository.update(task_id, title, done)
        return task, None

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)