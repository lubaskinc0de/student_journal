from abc import abstractmethod
from typing import Protocol

from student_journal.application.models.subject import SubjectReadModel
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.subject_id import SubjectId


class SubjectGateway(Protocol):
    @abstractmethod
    def read_subject(self, subject_id: SubjectId) -> Subject: ...

    @abstractmethod
    def write_subject(self, subject: Subject) -> None: ...

    @abstractmethod
    def read_subjects(
        self,
        sort_by_title: bool = False,
        sort_by_avg_mark: bool = False,
        show_empty: bool = True,
    ) -> list[SubjectReadModel]: ...

    @abstractmethod
    def update_subject(self, subject: Subject) -> None: ...

    @abstractmethod
    def delete_subject(self, subject_id: SubjectId) -> None: ...
