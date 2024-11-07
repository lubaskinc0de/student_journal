from dataclasses import dataclass
from datetime import date

from student_journal.domain.lesson import Lesson


@dataclass(frozen=True, slots=True)
class WeekLessons:
    week_start: date
    lessons: dict[date, Lesson]
    week_end: date


@dataclass(frozen=True, slots=True)
class LessonsByDate:
    lessons: dict[date, Lesson]
