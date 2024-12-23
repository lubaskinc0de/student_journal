from abc import abstractmethod
from typing import Protocol

from student_journal.application.models.home_task import HomeTaskReadModel
from student_journal.domain.home_task import HomeTask
from student_journal.domain.value_object.task_id import HomeTaskId


class HomeTaskGateway(Protocol):
    @abstractmethod
    def read_home_task(self, task_id: HomeTaskId) -> HomeTask: ...

    @abstractmethod
    def read_home_tasks(
        self,
        *,
        show_done: bool = False,
    ) -> list[HomeTaskReadModel]: ...

    @abstractmethod
    def write_home_task(self, home_task: HomeTask) -> None: ...

    @abstractmethod
    def update_home_task(self, home_task: HomeTask) -> None: ...

    @abstractmethod
    def delete_home_task(self, task_id: HomeTaskId) -> None: ...
