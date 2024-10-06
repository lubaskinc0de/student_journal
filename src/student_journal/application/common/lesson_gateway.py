from abc import abstractmethod
from typing import Protocol

from student_journal.domain.lesson import Lesson
from student_journal.domain.value_object.lesson_id import LessonId


class LessonGateway(Protocol):
    @abstractmethod
    def read_lesson(self, lesson_id: LessonId) -> Lesson: ...

    @abstractmethod
    def write_lesson(self, lesson: Lesson) -> LessonId: ...

    @abstractmethod
    def update_lesson(self, lesson: Lesson) -> None: ...

    @abstractmethod
    def delete_lesson(self, lesson_id: LessonId) -> None: ...
