from dataclasses import dataclass

from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.models.lesson import LessonsByDate


@dataclass(slots=True, frozen=True)
class ReadFirstLessonsOfWeeks:
    gateway: LessonGateway

    def execute(self) -> LessonsByDate:
        return self.gateway.read_first_lessons_of_weeks()
