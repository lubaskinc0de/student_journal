from abc import abstractmethod
from sqlite3 import OperationalError
from typing import Final, Protocol

from student_journal.adapters.exceptions.ui.hometask import DescriptionNotSpecifiedError
from student_journal.adapters.exceptions.ui.lesson import (
    LessonAtIsNotSpecifiedError,
    LessonIsNotSpecifiedError,
    SubjectIsNotSelectedError,
)
from student_journal.adapters.exceptions.ui.schedule import (
    CannotCopyScheduleError,
    WeekPeriodUnsetError,
    WeekStartUnsetError,
)
from student_journal.adapters.exceptions.ui.student import NameNotSpecifiedError
from student_journal.adapters.exceptions.ui.subject import (
    SubjectIsNotSpecifiedError,
    TeacherIsNotSelectedError,
    TitleIsNotSpecifiedError,
)
from student_journal.adapters.exceptions.ui.teacher import (
    FullNameNotSpecifiedError,
    TeacherIsNotSpecifiedError,
)
from student_journal.application.exceptions.base import ApplicationError
from student_journal.application.exceptions.home_task import (
    HomeTaskDescriptionError,
    HomeTaskNotFoundError,
)
from student_journal.application.exceptions.lesson import (
    LessonAlreadyExistError,
    LessonMarkError,
    LessonNoteError,
    LessonNotFoundError,
    LessonRoomError,
    LessonSubjectError,
)
from student_journal.application.exceptions.student import (
    StudentAgeError,
    StudentAlreadyExistError,
    StudentAvatarDoesNotExistsError,
    StudentHomeAddressError,
    StudentIsNotAuthenticatedError,
    StudentNameError,
    StudentNotFoundError,
    StudentTimezoneError,
)
from student_journal.application.exceptions.subject import (
    SubjectAlreadyExistsError,
    SubjectNotFoundError,
    SubjectTitleError,
)
from student_journal.application.exceptions.teacher import (
    TeacherAlreadyExistsError,
    TeacherFullNameError,
    TeacherNotFoundError,
)

_messages: Final[dict[type[ApplicationError | OperationalError], str]] = {
    HomeTaskDescriptionError: "Неверное описание домашнего задания",
    HomeTaskNotFoundError: "Домашнее задание не существует",
    LessonSubjectError: "Неверный предмет урока",
    LessonMarkError: "Неверная оценка урока",
    LessonNoteError: "Неверная заметка урока",
    LessonRoomError: "Неверный номер аудитории",
    LessonNotFoundError: "Урок не существует",
    LessonAlreadyExistError: "Урок уже существует",
    LessonAtIsNotSpecifiedError: "Время урока не указано",
    StudentNameError: "Неверное имя студента",
    StudentAgeError: "Неверный возраст студента",
    StudentHomeAddressError: "Неверный адрес студента",
    StudentAvatarDoesNotExistsError: "Аватар студента не существует",
    StudentNotFoundError: "Студент не существует",
    StudentAlreadyExistError: "Студент уже существует",
    StudentTimezoneError: "Неверная временная зона студента",
    StudentIsNotAuthenticatedError: "Студент не аутентифицирован",
    SubjectTitleError: "Неверное название предмета",
    SubjectAlreadyExistsError: "Предмет уже существует",
    SubjectNotFoundError: "Предмет не существует",
    TeacherFullNameError: "Неверное полное имя учителя",
    TeacherNotFoundError: "Учитель не существует",
    TeacherAlreadyExistsError: "Учитель уже существует",
    OperationalError: "Ошибка целостности БД!",
    DescriptionNotSpecifiedError: "Необходимо указать описание!",
    LessonIsNotSpecifiedError: "Урок не указан",
    SubjectIsNotSelectedError: "Предмет не выбран",
    WeekStartUnsetError: "Необходимо выбрать неделю",
    WeekPeriodUnsetError: "Необходимо выбрать месяц и год",
    NameNotSpecifiedError: "Имя студента не указано",
    TeacherIsNotSelectedError: "Учитель не выбран",
    TitleIsNotSpecifiedError: "Название предмета не указано",
    SubjectIsNotSpecifiedError: "Предмет не указан",
    FullNameNotSpecifiedError: "Полное имя учителя не указано",
    TeacherIsNotSpecifiedError: "Учитель не указан",
    CannotCopyScheduleError: "Невозможно скопировать расписание, "
    "так как в следующей неделе уже есть уроки.",
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
