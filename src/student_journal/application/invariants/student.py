from pathlib import Path

from student_journal.application.exceptions.student import (
    StudentAgeError,
    StudentAvatarNotExistsError,
    StudentHomeAddressError,
    StudentNameError,
    StudentTimezoneError,
)

MIN_AGE = 6
MAX_AGE = 100
AGE_RANGE = range(MIN_AGE, MAX_AGE)
NAME_MAX_LENGTH = 255
NAME_MIN_LENGTH = 2
HOME_ADDRESS_MAX_LENGTH = 255
TIMEZONE_RANGE = range(24)


def validate_student_invariants(
    age: int | None,
    name: str,
    home_address: str | None,
    avatar: str | None,
    timezone: int,
) -> None:
    if age and age not in AGE_RANGE:
        raise StudentAgeError

    if len(name) > NAME_MAX_LENGTH or len(name) < NAME_MIN_LENGTH:
        raise StudentNameError

    if home_address and len(home_address) > HOME_ADDRESS_MAX_LENGTH:
        raise StudentHomeAddressError

    if timezone not in TIMEZONE_RANGE:
        raise StudentTimezoneError

    if avatar and not Path(avatar).exists():
        raise StudentAvatarNotExistsError
