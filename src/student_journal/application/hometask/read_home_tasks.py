from dataclasses import dataclass

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.id_provider import IdProvider
from student_journal.application.models.home_task import HomeTasksReadModel


@dataclass(slots=True)
class ReadHomeTasks:
    gateway: HomeTaskGateway
    idp: IdProvider

    def execute(self, is_done: bool | None = False) -> HomeTasksReadModel:
        student_id = self.idp.get_id()
        home_tasks = self.gateway.read_home_tasks(is_done)

        return HomeTasksReadModel(
            student_id=student_id,
            home_tasks=home_tasks,
        )
