from .base import ApplicationError


class StudentNameError(ApplicationError): ...


class StudentAgeError(ApplicationError): ...


class StudentHomeAddressError(ApplicationError): ...


class StudentAvatarDoesNotExistsError(ApplicationError): ...


class StudentDoesNotExistError(ApplicationError): ...


class StudentAlreadyExistError(ApplicationError): ...


class StudentTimezoneError(ApplicationError): ...


class StudentIsNotAuthenticatedError(ApplicationError): ...
