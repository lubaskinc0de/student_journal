from abc import abstractmethod
from typing import Protocol

from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.teacher_id import TeacherId


class TeacherGateway(Protocol):
    @abstractmethod
    def read_teacher(self, teacher_id: Teacher) -> TeacherId: ...

    @abstractmethod
    def write_teacher(self, teacher: Teacher) -> None: ...
