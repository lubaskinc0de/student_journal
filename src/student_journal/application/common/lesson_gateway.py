from abc import abstractmethod
from datetime import date
from typing import Protocol

from student_journal.application.models.lesson import LessonsByDate, WeekLessons
from student_journal.domain.lesson import Lesson
from student_journal.domain.value_object.lesson_id import LessonId


class LessonGateway(Protocol):
    @abstractmethod
    def read_lesson(self, lesson_id: LessonId) -> Lesson: ...

    @abstractmethod
    def write_lesson(self, lesson: Lesson) -> None: ...

    @abstractmethod
    def update_lesson(self, lesson: Lesson) -> None: ...

    @abstractmethod
    def delete_lesson(self, lesson_id: LessonId) -> None: ...

    @abstractmethod
    def read_lessons_for_week(self, week_start: date) -> WeekLessons: ...

    @abstractmethod
    def read_first_lessons_of_weeks(self) -> LessonsByDate: ...
