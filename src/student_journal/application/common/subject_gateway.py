from abc import abstractmethod
from typing import Protocol

from student_journal.domain.subject import Subject
from student_journal.domain.value_object.subject_id import SubjectId


class SubjectGateway(Protocol):
    @abstractmethod
    def read_subject(self, subject_id: SubjectId) -> Subject: ...

    @abstractmethod
    def write_subject(self, subject: Subject) -> None: ...
