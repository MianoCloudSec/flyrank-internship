from app_v3.models import Task
from app_v3.repositories.base import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._tasks: list[Task] = [
            Task(id=1, title="Buy milk", done=False),
            Task(id=2, title="Walk the dog", done=False),
            Task(id=3, title="Finish W2 assignment", done=True),
        ]

    def get_all(self) -> list[Task]:
        return self._tasks

    def get_by_id(self, task_id: int) -> Task | None:
        return next((t for t in self._tasks if t.id == task_id), None)

    def create(self, title: str) -> Task:
        next_id = max((t.id for t in self._tasks), default=0) + 1
        task = Task(id=next_id, title=title, done=False)
        self._tasks.append(task)
        return task

    def update(self, task_id: int, title: str, done: bool) -> Task | None:
        task = self.get_by_id(task_id)
        if task is None:
            return None
        task.title = title
        task.done = done
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True