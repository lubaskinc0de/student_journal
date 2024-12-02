from abc import abstractmethod
from typing import Protocol

from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


class StudentGateway(Protocol):
    def read_student(self, student_id: StudentId) -> Student: ...

    @abstractmethod
    def write_student(self, student: Student) -> None: ...

    @abstractmethod
    def get_overall_avg_mark(self) -> float: ...

    @abstractmethod
    def update_student(self, student: Student) -> None: ...
