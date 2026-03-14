from dataclasses import dataclass

from student_journal.domain.access_service.generic import StudentAccessService
from student_journal.domain.entity.student import Student
from student_journal.domain.entity.subject import Subject
from student_journal.domain.exception.access import AccessDeniedError


@dataclass(slots=True, frozen=True)
class SubjectAccessService(StudentAccessService[Subject]):
    student: Student

    def ensure_has_access(self, obj: Subject) -> None:
        if obj.student_id != self.student.student_id:
            raise AccessDeniedError
