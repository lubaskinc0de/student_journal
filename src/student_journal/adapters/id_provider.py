from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.domain.value_object.student_id import StudentId


@dataclass(slots=True, frozen=True)
class SimpleIdProvider(IdProvider):
    student_id: StudentId

    def get_id(self) -> StudentId:
        return self.student_id
