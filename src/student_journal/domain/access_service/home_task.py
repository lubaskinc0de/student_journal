from dataclasses import dataclass

from student_journal.domain.access_service.generic import StudentAccessService
from student_journal.domain.entity.home_task import HomeTask
from student_journal.domain.entity.student import Student
from student_journal.domain.exception.access import AccessDeniedError


@dataclass(slots=True, frozen=True)
class HomeTaskAccessService(StudentAccessService[HomeTask]):
    student: Student

    def ensure_has_access(self, obj: HomeTask) -> None:
        if obj.student_id != self.student.student_id:
            raise AccessDeniedError
