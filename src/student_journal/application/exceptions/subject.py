from .base import ApplicationError


class SubjectTitleError(ApplicationError): ...


class SubjectAlreadyExistsError(SubjectTitleError): ...


class SubjectDoesNotExistError(SubjectTitleError): ...
