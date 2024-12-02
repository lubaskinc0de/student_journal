from pathlib import Path

from student_journal.application.exceptions.student import (
    StudentAgeError,
    StudentAvatarDoesNotExistsError,
    StudentHomeAddressError,
    StudentNameError,
)

MIN_AGE = 6
MAX_AGE = 100
AGE_RANGE = range(MIN_AGE, MAX_AGE + 1)
NAME_MAX_LENGTH = 60
NAME_MIN_LENGTH = 2
HOME_ADDRESS_MAX_LENGTH = 255
HOME_ADDRESS_MIN_LENGTH = 2


def validate_student_invariants(
    age: int | None,
    name: str,
    home_address: str | None,
    avatar: str | None,
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

    if (avatar is not None) and not Path(avatar).exists():
        raise StudentAvatarDoesNotExistsError
