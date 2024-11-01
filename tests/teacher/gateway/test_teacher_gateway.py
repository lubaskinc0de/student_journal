from sqlite3 import Cursor

import pytest
from student_journal.adapters.models.teacher import teacher_retort
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.exceptions.teacher import TeacherDoesNotExistError
from student_journal.domain.teacher import Teacher

from teacher.confest import TEACHER, TEACHER_ID

READ_TEACHER_SQL = "SELECT * FROM Teacher"


def test_write(
    teacher_gateway: TeacherGateway,
    cursor: Cursor,
) -> None:
    teacher_gateway.write_teacher(TEACHER)
    db_teacher = teacher_retort.load(
        dict(cursor.execute(READ_TEACHER_SQL).fetchone()),
        Teacher,
    )

    assert db_teacher == TEACHER


def test_read(
    teacher_gateway: TeacherGateway,
    cursor: Cursor,
) -> None:
    teacher_gateway.write_teacher(TEACHER)
    db_teacher = teacher_retort.load(
        dict(cursor.execute(READ_TEACHER_SQL).fetchone()),
        Teacher,
    )

    assert db_teacher == teacher_gateway.read_teacher(TEACHER_ID)


def test_read_not_exist(
    teacher_gateway: TeacherGateway,
    cursor: Cursor,
) -> None:
    with pytest.raises(TeacherDoesNotExistError):
        teacher_gateway.read_teacher(TEACHER_ID)


def test_update(
    teacher_gateway: TeacherGateway,
    cursor: Cursor,
) -> None:
    teacher_gateway.write_teacher(TEACHER)
    updated_teacher = Teacher(
        teacher_id=TEACHER_ID,
        full_name="testtest",
        avatar=None,
    )

    teacher_gateway.update_teacher(updated_teacher)
    db_teacher = teacher_retort.load(
        dict(cursor.execute(READ_TEACHER_SQL).fetchone()),
        Teacher,
    )

    assert db_teacher == updated_teacher
