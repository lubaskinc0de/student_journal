from dataclasses import dataclass
from datetime import date, datetime

from student_journal.domain.lesson import Lesson


@dataclass(frozen=True, slots=True)
class WeekLessons:
    week_start: date
    lessons: dict[date, list[Lesson]]
    week_end: date


@dataclass(frozen=True, slots=True)
class LessonsByDate:
    lessons: dict[datetime, Lesson]
