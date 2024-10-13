import string

import pytest
from student_journal.application.exceptions.base import ApplicationError
from student_journal.application.exceptions.student import (
    StudentAgeError,
    StudentAvatarNotExistsError,
    StudentHomeAddressError,
    StudentNameError,
    StudentTimezoneError,
)
from student_journal.application.invariants.student import (
    HOME_ADDRESS_MAX_LENGTH,
    MAX_AGE,
    MIN_AGE,
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
)
from student_journal.application.student.create_student import CreateStudent, NewStudent

from tests.unit.mock.transaction_manager import MockedTransactionManager


def test_create_student(
    create_student: CreateStudent,
    transaction_manager: MockedTransactionManager,
) -> None:
    data = NewStudent(
        age=14,
        avatar=None,
        name="Ilya",
        home_address=None,
    )

    create_student.execute(data)

    assert transaction_manager.is_begin
    assert transaction_manager.is_commited


@pytest.mark.parametrize(
    ("age", "name", "home_address", "avatar", "exc_class", "timezone"),
    [
        (MIN_AGE - 1, "Ilya", None, None, StudentAgeError, 0),
        (MAX_AGE, "Ilya", None, None, StudentAgeError, 0),
        (14, (NAME_MAX_LENGTH + 1) * "a", None, None, StudentNameError, 0),
        (14, (NAME_MIN_LENGTH - 1) * "a", None, None, StudentNameError, 0),
        (
            14,
            "Ilya",
            (HOME_ADDRESS_MAX_LENGTH + 1) * "a",
            None,
            StudentHomeAddressError,
            0,
        ),
        (14, "Ilya", None, None, StudentTimezoneError, 28),
        (14, "Ilya", None, string.ascii_letters, StudentAvatarNotExistsError, 0),
    ],
)
def test_create_student_bad_invariants(
    create_student: CreateStudent,
    age: int,
    name: str,
    home_address: str | None,
    avatar: str | None,
    exc_class: type[ApplicationError],
    timezone: int,
) -> None:
    data = NewStudent(
        age=age,
        avatar=avatar,
        name=name,
        home_address=home_address,
        timezone=timezone,
    )

    with pytest.raises(exc_class):
        create_student.execute(data)
