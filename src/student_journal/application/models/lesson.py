from dataclasses import dataclass
from datetime import datetime

from student_journal.domain.lesson import Lesson


@dataclass(frozen=True, slots=True)
class WeekLessons:
    week_start: datetime
    lessons: dict[datetime, Lesson]
    week_end: datetime


@dataclass(frozen=True, slots=True)
class LessonsByDate:
    lessons: dict[datetime, Lesson]
