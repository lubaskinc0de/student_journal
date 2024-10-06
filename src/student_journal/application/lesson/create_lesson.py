from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.lesson import (
    LessonAtError,
    LessonIndexNumberError,
    LessonMarkError,
    LessonNoteError,
    LessonRoomError,
)
from student_journal.domain.lesson import Lesson
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True, frozen=True)
class NewLesson:
    subject_id: SubjectId
    at: datetime
    mark: int | None
    note: str | None
    room: int
    index_number: int


@dataclass(slots=True)
class CreateLesson:
    gateway: LessonGateway
    student_gateway: StudentGateway
    transaction_manager: TransactionManager
    idp: IdProvider

    def execute(self, data: NewLesson) -> LessonId:
        self.transaction_manager.begin()
        student = self.student_gateway.read_student(self.idp.get_id())

        if data.at < (datetime.now(tz=UTC) + timedelta(hours=student.timezone)):
            raise LessonAtError()

        if data.mark and not (0 < data.mark <= 5):
            raise LessonMarkError()

        if data.note and len(data.note) > 65535:
            raise LessonNoteError()

        if data.room < 1:
            raise LessonRoomError()

        if data.index_number < 0:
            raise LessonIndexNumberError()

        lesson_id = LessonId(uuid4())
        lesson = Lesson(
            lesson_id=lesson_id,
            subject_id=data.subject_id,
            at=data.at,
            mark=data.mark,
            note=data.note,
            room=data.room,
            index_number=data.index_number,
        )

        self.gateway.write_lesson(lesson)
        self.transaction_manager.commit()

        return lesson_id
