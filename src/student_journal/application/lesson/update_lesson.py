from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.exceptions.lesson import (
    LessonAtError,
    LessonDoesNotExistError,
    LessonIdError,
    LessonIndexNumberError,
    LessonMarkError,
    LessonNoteError,
    LessonRoomError,
    LessonSubjectError,
)
from student_journal.domain.lesson import Lesson
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True, frozen=True)
class UpdatedLesson:
    lesson_id: LessonId
    subject_id: SubjectId
    at: datetime
    mark: int | None
    note: str | None
    room: int
    index_number: int


@dataclass(slots=True)
class UpdateLesson:
    gateway: LessonGateway
    transaction_manager: TransactionManager

    def execute(self, data: UpdatedLesson) -> LessonId:
        if not data.lesson_id:
            raise LessonIdError()

        if not self.gateway.read_lesson(data.lesson_id):  # ! Возможно будущее изменение
            raise LessonDoesNotExistError()

        if not data.subject_id:
            raise LessonSubjectError()

        # TODO: сделать проверку на сущестование subject

        if data.at < datetime.now():
            raise LessonAtError()

        if data.mark and not (0 < data.mark <= 5):
            raise LessonMarkError()

        if data.note and len(data.note) > 65535:
            raise LessonNoteError()

        if data.room < 0:
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

        self.transaction_manager.begin()
        self.gateway.update_lesson(lesson)
        self.transaction_manager.commit()

        return lesson_id
