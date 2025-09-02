from dataclasses import dataclass

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.models.home_task import HomeTaskReadModel


@dataclass(slots=True)
class ReadHomeTasks:
    gateway: HomeTaskGateway
    idp: StudentIdProvider

    def execute(self, *, show_done: bool = False) -> list[HomeTaskReadModel]:
        student_id = self.idp.get_student_id()
        home_tasks = self.gateway.read_home_tasks(
            show_done=show_done,
            student_id=student_id,
        )

        return home_tasks
