from dataclasses import dataclass

from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.domain.value_object.task_id import HomeTaskId


@dataclass(slots=True)
class DeleteHomeTask:
    transaction_manager: TransactionManager
    gateway: HomeTaskGateway
    idp: IdProvider

    def execute(self, task_id: HomeTaskId) -> None:
        self.idp.ensure_is_auth()

        with self.transaction_manager.begin():
            self.gateway.delete_home_task(task_id)
            self.transaction_manager.commit()
