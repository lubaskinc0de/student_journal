from abc import abstractmethod
from typing import Protocol

from student_journal.domain.entity.teacher import Teacher
from student_journal.domain.id_type.student_id import StudentId
from student_journal.domain.id_type.teacher_id import TeacherId


class TeacherGateway(Protocol):
    @abstractmethod
    def read_teacher(self, teacher_id: TeacherId) -> Teacher | None: ...

    @abstractmethod
    def write_teacher(self, teacher: Teacher) -> None: ...

    @abstractmethod
    def read_teachers(self, student_id: StudentId) -> list[Teacher]: ...

    @abstractmethod
    def update_teacher(self, teacher: Teacher) -> None: ...

    @abstractmethod
    def delete_teacher(self, teacher_id: TeacherId) -> None: ...
