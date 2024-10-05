from .base import ApplicationError


class TeacherFullNameError(ApplicationError): ...


class TeacherDoesNotExistError(ApplicationError): ...


class TeacherAlreadyExistsError(ApplicationError): ...
