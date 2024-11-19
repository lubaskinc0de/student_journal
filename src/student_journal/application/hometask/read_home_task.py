from dataclasses import dataclass

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.id_provider import IdProvider
from student_journal.domain.home_task import HomeTask
from student_journal.domain.value_object.task_id import HomeTaskId


@dataclass(slots=True)
class ReadHomeTask:
    gateway: HomeTaskGateway
    idp: IdProvider

    def execute(self, task_id: HomeTaskId) -> HomeTask:
        self.idp.ensure_is_auth()

        home_task = self.gateway.read_home_task(task_id)
        return home_task
