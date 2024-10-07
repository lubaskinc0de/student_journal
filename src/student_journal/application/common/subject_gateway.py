from abc import abstractmethod
from typing import Protocol

from student_journal.application.models.subject import SubjectReadModel
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.student_id import StudentId
from student_journal.domain.value_object.subject_id import SubjectId


class SubjectGateway(Protocol):
    @abstractmethod
    def read_subject(self, subject_id: SubjectId) -> Subject: ...

    @abstractmethod
    def write_subject(self, subject: Subject) -> None: ...

    @abstractmethod
    def read_subjects(self, student_id: StudentId) -> list[SubjectReadModel]: ...

    @abstractmethod
    def update_subject(self, subject: Subject) -> None: ...

    @abstractmethod
    def delete_subject(self, subject_id: SubjectId) -> None: ...
