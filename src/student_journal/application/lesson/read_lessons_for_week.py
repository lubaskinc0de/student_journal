from dataclasses import dataclass
from datetime import datetime

from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.models.lesson import WeekLessons


@dataclass(slots=True, frozen=True)
class ReadLessonsForWeek:
    gateway: LessonGateway
    idp: IdProvider

    def execute(self, week_start: datetime) -> WeekLessons:
        self.idp.ensure_authenticated()
        return self.gateway.read_lessons_for_week(week_start)
