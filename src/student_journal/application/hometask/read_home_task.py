from dataclasses import dataclass

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.exceptions.home_task import HomeTaskNotFoundError
from student_journal.domain.entity.home_task import HomeTask
from student_journal.domain.exception.access import AccessDeniedError
from student_journal.domain.id_type.task_id import HomeTaskId


@dataclass(slots=True)
class ReadHomeTask:
    gateway: HomeTaskGateway
    idp: StudentIdProvider

    def execute(self, task_id: HomeTaskId) -> HomeTask:
        self.idp.require_auth()

        home_task = self.gateway.read_home_task(task_id)

        if not home_task:
            raise HomeTaskNotFoundError

        if not home_task.can_view(self.idp.get_student_id()):
            raise AccessDeniedError

        return home_task
