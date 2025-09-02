from abc import abstractmethod
from datetime import date, timezone
from typing import Protocol

from student_journal.application.models.lesson import LessonsByDate, WeekLessons
from student_journal.domain.entity.lesson import Lesson
from student_journal.domain.entity.subject import Subject
from student_journal.domain.id_type.lesson_id import LessonId
from student_journal.domain.id_type.student_id import StudentId


class LessonGateway(Protocol):
    @abstractmethod
    def read_lesson(
        self,
        lesson_id: LessonId,
        as_tz: timezone,
    ) -> Lesson | None: ...

    @abstractmethod
    def write_lesson(
        self,
        lesson: Lesson,
    ) -> None: ...

    @abstractmethod
    def update_lesson(
        self,
        lesson: Lesson,
    ) -> None: ...

    @abstractmethod
    def delete_lesson(self, lesson_id: LessonId) -> None: ...

    @abstractmethod
    def read_lessons_for_week(
        self,
        week_start: date,
        as_tz: timezone,
        student_id: StudentId,
    ) -> WeekLessons: ...

    @abstractmethod
    def read_first_lessons_of_weeks(
        self,
        month: int,
        year: int,
        as_tz: timezone,
        student_id: StudentId,
    ) -> LessonsByDate: ...

    @abstractmethod
    def read_subjects_for_lessons(
        self,
        lessons: list[LessonId],
    ) -> dict[LessonId, Subject]: ...

    @abstractmethod
    def delete_lessons(self, lessons: list[LessonId]) -> None: ...

    @abstractmethod
    def delete_all_lessons(self) -> None: ...
