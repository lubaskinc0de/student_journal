from student_journal.application.exceptions.student import (
    StudentAgeError,
    StudentHomeAddressError,
    StudentNameError,
    StudentTimezoneError,
)

AGE_RANGE = range(6, 100)
NAME_MAX_LENGTH = 255
HOME_ADDRESS_MAX_LENGTH = 255
TIMEZONE_RANGE = range(24)


def validate_student_invariants(
    age: int | None,
    name: str,
    home_address: str | None,
    timezone: int,
) -> None:
    if age and age not in AGE_RANGE:
        raise StudentAgeError

    if len(name) > NAME_MAX_LENGTH:
        raise StudentNameError

    if home_address and len(home_address) > HOME_ADDRESS_MAX_LENGTH:
        raise StudentHomeAddressError

    if timezone not in TIMEZONE_RANGE:
        raise StudentTimezoneError
