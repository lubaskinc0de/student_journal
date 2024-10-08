from abc import abstractmethod
from typing import Protocol

from student_journal.domain.home_task import HomeTask
from student_journal.domain.value_object.task_id import TaskId


class HomeTaskGateway(Protocol):
    @abstractmethod
    def read_home_task(self, task_id: TaskId) -> HomeTask: ...

    @abstractmethod
    def write_home_task(self, home_task: HomeTask) -> None: ...

    @abstractmethod
    def update_home_task(self, home_task: HomeTask) -> None: ...

    @abstractmethod
    def delete_home_task(self, task_id: TaskId) -> None: ...
