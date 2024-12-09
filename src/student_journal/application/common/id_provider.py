from abc import abstractmethod
from typing import Protocol

from student_journal.domain.id_type.student_id import StudentId


class StudentIdProvider(Protocol):
    @abstractmethod
    def get_id(self) -> StudentId: ...

    @abstractmethod
    def ensure_auth(self) -> None: ...
