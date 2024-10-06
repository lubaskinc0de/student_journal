from .base import ApplicationError


class LessonIdError(ApplicationError):
    "Raised when the lesson id is invalid"


class LessonSubjectError(ApplicationError): ...


class LessonAtError(ApplicationError): ...


class LessonMarkError(ApplicationError): ...


class LessonNoteError(ApplicationError): ...


class LessonRoomError(ApplicationError): ...


class LessonIndexNumberError(ApplicationError): ...


class LessonDoesNotExistError(ApplicationError): ...


class LessonAlreadyExistError(ApplicationError): ...
