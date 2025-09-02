from abc import abstractmethod
from typing import Protocol

from student_journal.domain.id_type.student_id import StudentId


class StudentIdProvider(Protocol):
    @abstractmethod
    def get_student_id(self) -> StudentId: ...

    @abstractmethod
    def require_auth(self) -> None: ...
