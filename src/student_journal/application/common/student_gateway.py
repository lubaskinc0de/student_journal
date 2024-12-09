from abc import abstractmethod
from typing import Protocol

from student_journal.domain.id_type.student_id import StudentId
from student_journal.domain.entity.student import Student


class StudentGateway(Protocol):
    def read_student(self, student_id: StudentId) -> Student | None: ...

    @abstractmethod
    def write_student(self, student: Student) -> None: ...

    @abstractmethod
    def get_overall_avg_mark(self) -> float: ...

    @abstractmethod
    def update_student(self, student: Student) -> None: ...
