from abc import abstractmethod
from typing import Protocol

from student_journal.domain.value_object.student_id import StudentId


class IdProvider(Protocol):
    @abstractmethod
    def get_id(self) -> StudentId: ...
