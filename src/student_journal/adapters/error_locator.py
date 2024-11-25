from abc import abstractmethod
from sqlite3 import OperationalError
from typing import Final, Protocol

from student_journal.application.exceptions.base import ApplicationError
from student_journal.application.exceptions.home_task import (
    HomeTaskDescriptionError,
    HomeTaskDoesNotExistError,
)
from student_journal.application.exceptions.lesson import (
    LessonAlreadyExistError,
    LessonAtError,
    LessonDoesNotExistError,
    LessonIndexNumberError,
    LessonMarkError,
    LessonNoteError,
    LessonRoomError,
    LessonSubjectError,
)
from student_journal.application.exceptions.student import (
    StudentAgeError,
    StudentAlreadyExistError,
    StudentAvatarDoesNotExistsError,
    StudentDoesNotExistError,
    StudentHomeAddressError,
    StudentIsNotAuthenticatedError,
    StudentNameError,
    StudentTimezoneError,
)
from student_journal.application.exceptions.subject import (
    SubjectAlreadyExistsError,
    SubjectDoesNotExistError,
    SubjectTitleError,
)
from student_journal.application.exceptions.teacher import (
    TeacherAlreadyExistsError,
    TeacherDoesNotExistError,
    TeacherFullNameError,
)

_messages: Final[dict[type[ApplicationError | OperationalError], str]] = {
    HomeTaskDescriptionError: "Неверное описание домашнего задания",
    HomeTaskDoesNotExistError: "Домашнее задание не существует",
    LessonSubjectError: "Неверный предмет урока",
    LessonAtError: "Неверное время урока",
    LessonMarkError: "Неверная оценка урока",
    LessonNoteError: "Неверная заметка урока",
    LessonRoomError: "Неверный номер аудитории",
    LessonIndexNumberError: "Неверный индекс урока",
    LessonDoesNotExistError: "Урок не существует",
    LessonAlreadyExistError: "Урок уже существует",
    StudentNameError: "Неверное имя студента",
    StudentAgeError: "Неверный возраст студента",
    StudentHomeAddressError: "Неверный адрес студента",
    StudentAvatarDoesNotExistsError: "Аватар студента не существует",
    StudentDoesNotExistError: "Студент не существует",
    StudentAlreadyExistError: "Студент уже существует",
    StudentTimezoneError: "Неверная временная зона студента",
    StudentIsNotAuthenticatedError: "Студент не аутентифицирован",
    SubjectTitleError: "Неверное название предмета",
    SubjectAlreadyExistsError: "Предмет уже существует",
    SubjectDoesNotExistError: "Предмет не существует",
    TeacherFullNameError: "Неверное полное имя учителя",
    TeacherDoesNotExistError: "Учитель не существует",
    TeacherAlreadyExistsError: "Учитель уже существует",
    OperationalError: "Ошибка целостности БД!",
}


class ErrorLocator(Protocol):
    @abstractmethod
    def get_text(self, error: ApplicationError) -> str: ...


class SimpleErrorLocator(ErrorLocator):
    def get_text(self, error: ApplicationError) -> str:
        try:
            return _messages[type(error)]
        except KeyError:
            return error.__class__.__qualname__
