import string

import pytest
from common.mock.transaction_manager import MockedTransactionManager

from student_journal.application.exceptions.base import ApplicationError
from student_journal.application.exceptions.student import (
    StudentAgeError,
    StudentAvatarDoesNotExistsError,
    StudentHomeAddressError,
    StudentNameError,
)
from student_journal.application.invariants.student import (
    HOME_ADDRESS_MAX_LENGTH,
    MAX_AGE,
    MIN_AGE,
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
)
from student_journal.application.student.create_student import CreateStudent, NewStudent
from student_journal.application.student.read_student import ReadStudent
from student_journal.application.student.update_student import (
    UpdatedStudent,
    UpdateStudent,
)
from unit.conftest import STUDENT, STUDENT_ID
from unit.student.mock.student_gateway import MockedStudentGateway

BAD_INVARIANTS = (
    [
        (MIN_AGE - 1, "Ilya", None, None, StudentAgeError),
        (MAX_AGE, "Ilya", None, None, StudentAgeError),
        (14, (NAME_MAX_LENGTH + 1) * "a", None, None, StudentNameError),
        (14, (NAME_MIN_LENGTH - 1) * "a", None, None, StudentNameError),
        (
            14,
            "Ilya",
            (HOME_ADDRESS_MAX_LENGTH + 1) * "a",
            None,
            StudentHomeAddressError,
        ),
        (14, "Ilya", None, string.ascii_letters, StudentAvatarDoesNotExistsError),
    ],
)


def test_create_student(
    create_student: CreateStudent,
    transaction_manager: MockedTransactionManager,
    student_gateway: MockedStudentGateway,
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
    assert student_gateway.is_wrote


@pytest.mark.parametrize(
    ("age", "name", "home_address", "avatar", "exc_class"),
    *BAD_INVARIANTS,
)
def test_create_student_bad_invariants(
    create_student: CreateStudent,
    age: int,
    name: str,
    home_address: str | None,
    avatar: str | None,
    exc_class: type[ApplicationError],
) -> None:
    data = NewStudent(
        age=age,
        avatar=avatar,
        name=name,
        home_address=home_address,
    )

    with pytest.raises(exc_class):
        create_student.execute(data)


def test_read_student(
    read_student: ReadStudent,
    student_gateway: MockedStudentGateway,
) -> None:
    student_gateway.write_student(STUDENT)
    student = read_student.execute()

    assert student.student_id == STUDENT_ID
    assert student.student_overall_avg_mark == student_gateway.AVG_MARK


def test_update_student(
    update_student: UpdateStudent,
    student_gateway: MockedStudentGateway,
    transaction_manager: MockedTransactionManager,
) -> None:
    student_gateway.write_student(STUDENT)

    updated_id = update_student.execute(
        UpdatedStudent(
            age=STUDENT.age + 1,
            avatar=STUDENT.avatar,
            name=STUDENT.name,
            home_address=STUDENT.home_address,
        ),
    )

    assert student_gateway.is_updated
    assert transaction_manager.is_begin
    assert transaction_manager.is_commited
    assert updated_id == STUDENT_ID


@pytest.mark.parametrize(
    ("age", "name", "home_address", "avatar", "exc_class"),
    *BAD_INVARIANTS,
)
def test_update_student_bad_invariants(
    student_gateway: MockedStudentGateway,
    update_student: UpdateStudent,
    age: int,
    name: str,
    home_address: str | None,
    avatar: str | None,
    exc_class: type[ApplicationError],
) -> None:
    student_gateway.write_student(STUDENT)

    with pytest.raises(exc_class):
        update_student.execute(
            UpdatedStudent(
                age=age,
                avatar=avatar,
                name=name,
                home_address=home_address,
            ),
        )
