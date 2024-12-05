from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.models.subject import SubjectReadModel


@dataclass(slots=True)
class ReadSubjects:
    gateway: SubjectGateway
    idp: IdProvider

    def execute(
        self,
        *,
        sort_by_title: bool = False,
        sort_by_avg_mark: bool = False,
        show_empty: bool = True,
    ) -> list[SubjectReadModel]:
        self.idp.ensure_authenticated()

        subjects = self.gateway.read_subjects(
            sort_by_title=sort_by_title,
            sort_by_avg_mark=sort_by_avg_mark,
            show_empty=show_empty,
        )

        return subjects
