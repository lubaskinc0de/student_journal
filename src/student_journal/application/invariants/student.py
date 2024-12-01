from pathlib import Path

from student_journal.application.exceptions.student import (
    StudentAgeError,
    StudentAvatarDoesNotExistsError,
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
HOME_ADDRESS_MIN_LENGTH = 2
TIMEZONE_RANGE = range(-12, 15)


def validate_student_invariants(
    age: int | None,
    name: str,
    home_address: str | None,
    avatar: str | None,
    timezone: int,
) -> None:
    if (age is not None) and age not in AGE_RANGE:
        raise StudentAgeError

    if len(name) > NAME_MAX_LENGTH or len(name) < NAME_MIN_LENGTH:
        raise StudentNameError

    if home_address is not None and len(home_address) not in range(
        HOME_ADDRESS_MIN_LENGTH,
        HOME_ADDRESS_MAX_LENGTH,
    ):
        raise StudentHomeAddressError

    if timezone not in TIMEZONE_RANGE:
        raise StudentTimezoneError

    if (avatar is not None) and not Path(avatar).exists():
        raise StudentAvatarDoesNotExistsError
