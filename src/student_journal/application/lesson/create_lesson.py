from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.invariants.lesson import validate_lesson_invariants
from student_journal.domain.lesson import Lesson
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True, frozen=True)
class NewLesson:
    subject_id: SubjectId
    at: datetime
    mark: int | None
    note: str | None
    room: int = 1


@dataclass(slots=True)
class CreateLesson:
    gateway: LessonGateway
    student_gateway: StudentGateway
    transaction_manager: TransactionManager
    idp: IdProvider

    def execute(self, data: NewLesson) -> LessonId:
        student = self.student_gateway.read_student(self.idp.get_id())

        local_at = data.at.replace(tzinfo=student.get_timezone())

        validate_lesson_invariants(
            at=local_at,
            student_timezone=student.utc_offset,
            mark=data.mark,
            note=data.note,
            room=data.room,
        )

        lesson_id = LessonId(uuid4())
        lesson = Lesson(
            lesson_id=lesson_id,
            subject_id=data.subject_id,
            at=local_at,
            mark=data.mark,
            note=data.note,
            room=data.room,
        )

        with self.transaction_manager.begin():
            self.gateway.write_lesson(lesson)
            self.transaction_manager.commit()

        return lesson_id
