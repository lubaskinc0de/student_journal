from dataclasses import dataclass
from datetime import UTC, datetime

import structlog

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.logger import Logger, retort
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.lesson import LessonNotFoundError
from student_journal.application.exceptions.student import StudentNotFoundError
from student_journal.application.validators.lesson import validate_lesson
from student_journal.domain.entity.lesson import Lesson
from student_journal.domain.id_type.lesson_id import LessonId
from student_journal.domain.id_type.subject_id import SubjectId

logger: Logger = structlog.get_logger(__name__)


@dataclass(slots=True, frozen=True)
class UpdatedLesson:
    lesson_id: LessonId
    subject_id: SubjectId
    at: datetime
    mark: int | None
    note: str | None
    room: int


@dataclass(slots=True)
class UpdateLesson:
    gateway: LessonGateway
    student_gateway: StudentGateway
    transaction_manager: TransactionManager
    idp: StudentIdProvider

    def execute(self, data: UpdatedLesson) -> LessonId:
        student = self.student_gateway.read_student(self.idp.get_student_id())
        if not student:
            raise StudentNotFoundError

        orig_object = self.gateway.read_lesson(lesson_id=data.lesson_id, as_tz=UTC)
        if orig_object is None:
            raise LessonNotFoundError

        utc_at = data.at.astimezone(UTC)
        validate_lesson(
            mark=data.mark,
            note=data.note,
            room=data.room,
        )

        lesson = Lesson(
            lesson_id=data.lesson_id,
            subject_id=data.subject_id,
            at=utc_at,
            mark=data.mark,
            note=data.note,
            room=data.room,
            student_id=orig_object.student_id,
        )

        with self.transaction_manager.begin():
            self.gateway.update_lesson(lesson)
            self.transaction_manager.commit()

        logger.debug(
            "Updated lesson",
            old_data=retort.dump(orig_object),
            data=retort.dump(lesson),
            user_id=self.idp.get_student_id(),
        )
        return data.lesson_id
