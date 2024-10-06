from dataclasses import dataclass

from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.domain.value_object.lesson_id import LessonId


@dataclass(slots=True)
class DeleteLesson:
    gateway: LessonGateway

    def execute(self, lesson_id: LessonId) -> None:
        self.gateway.delete_lesson(lesson_id)
