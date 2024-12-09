from abc import abstractmethod
from typing import Protocol

from student_journal.application.models.home_task import HomeTaskReadModel
from student_journal.domain.entity.home_task import HomeTask
from student_journal.domain.id_type.student_id import StudentId
from student_journal.domain.id_type.task_id import HomeTaskId


class HomeTaskGateway(Protocol):
    @abstractmethod
    def read_home_task(
        self,
        task_id: HomeTaskId,
    ) -> HomeTask | None: ...

    @abstractmethod
    def read_home_tasks(
        self,
        student_id: StudentId,
        *,
        show_done: bool = False,
    ) -> list[HomeTaskReadModel]: ...

    @abstractmethod
    def write_home_task(
        self,
        home_task: HomeTask,
    ) -> None: ...

    @abstractmethod
    def update_home_task(self, home_task: HomeTask) -> None: ...

    @abstractmethod
    def delete_home_task(self, task_id: HomeTaskId) -> None: ...
