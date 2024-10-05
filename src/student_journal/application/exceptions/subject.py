from .base import ApplicationError


class SubjectTitleError(ApplicationError): ...


class SubjectAlreadyExistsError(SubjectTitleError): ...


class SubjectDoesNotExistsError(SubjectTitleError): ...
