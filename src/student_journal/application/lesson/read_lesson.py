from dataclasses import dataclass

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.domain.lesson import Lesson
from student_journal.domain.value_object.lesson_id import LessonId


@dataclass(slots=True)
class ReadLesson:
    gateway: LessonGateway
    idp: IdProvider

    def execute(self, lesson_id: LessonId) -> Lesson:
        self.idp.ensure_authenticated()

        lesson = self.gateway.read_lesson(lesson_id)
        return lesson
