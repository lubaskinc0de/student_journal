from adaptix.conversion import impl_converter

from student_journal.application.models.student import StudentReadModel
from student_journal.domain.student import Student


@impl_converter()
def convert_student_to_read_model(  # type: ignore
    student: Student,
    student_overall_avg_mark: float,
) -> StudentReadModel: ...
