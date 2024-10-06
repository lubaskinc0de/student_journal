from abc import abstractmethod
from typing import Protocol

from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


class StudentGateway(Protocol):
    @abstractmethod
    def read_student(self, student_id: StudentId) -> Student: ...

    @abstractmethod
    def write_student(self, student: Student) -> None: ...