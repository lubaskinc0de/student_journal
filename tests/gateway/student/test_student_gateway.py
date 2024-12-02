from sqlite3 import Cursor

import pytest

from student_journal.application.exceptions.student import StudentNotFoundError
from unit.conftest import STUDENT, STUDENT_ID

from student_journal.adapters.converter.student import student_retort
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.domain.student import Student

READ_STUDENT_SQL = "SELECT * FROM Student"


def test_write(
    student_gateway: StudentGateway,
    cursor: Cursor,
) -> None:
    student_gateway.write_student(STUDENT)
    db_student = student_retort.load(
        dict(cursor.execute(READ_STUDENT_SQL).fetchone()),
        Student,
    )

    assert db_student == STUDENT


def test_read(
    student_gateway: StudentGateway,
    cursor: Cursor,
) -> None:
    student_gateway.write_student(STUDENT)
    db_student = student_retort.load(
        dict(cursor.execute(READ_STUDENT_SQL).fetchone()),
        Student,
    )

    assert db_student == student_gateway.read_student(STUDENT_ID)


def test_read_not_exist(
    student_gateway: StudentGateway,
    cursor: Cursor,
) -> None:
    with pytest.raises(StudentNotFoundError):
        student_gateway.read_student(STUDENT_ID)


def test_update(
    student_gateway: StudentGateway,
    cursor: Cursor,
) -> None:
    student_gateway.write_student(STUDENT)
    updated_student = Student(
        name="abracadabra",
        age=75,
        home_address=None,
        avatar=None,
        student_id=STUDENT_ID,
    )

    student_gateway.update_student(updated_student)
    db_student = student_retort.load(
        dict(cursor.execute(READ_STUDENT_SQL).fetchone()),
        Student,
    )

    assert db_student == updated_student
