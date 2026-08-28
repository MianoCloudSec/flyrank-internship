from abc import ABC, abstractmethod
from app_v3.models import Task


class TaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Task]:
        ...

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        ...

    @abstractmethod
    def create(self, title: str) -> Task:
        ...

    @abstractmethod
    def update(self, task_id: int, title: str, done: bool) -> Task | None:
        ...

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        ...