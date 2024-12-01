from .base import ApplicationError


class TeacherFullNameError(ApplicationError): ...


class TeacherNotFoundError(ApplicationError): ...


class TeacherAlreadyExistsError(ApplicationError): ...
