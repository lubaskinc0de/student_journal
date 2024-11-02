import pytest
from student_journal.application.exceptions.base import ApplicationError
from student_journal.application.exceptions.teacher import (
    TeacherFullNameError,
)
from student_journal.application.invariants.teacher import FULL_NAME_MAX_LENGTH
from student_journal.application.models.teacher import TeachersReadModel
from student_journal.application.teacher import (
    CreateTeacher,
    DeleteTeacher,
    NewTeacher,
    ReadTeacher,
    ReadTeachers,
    UpdatedTeacher,
    UpdateTeacher,
)

from unit.student.mock import MockedTeacherGateway, MockedTransactionManager
from unit.teacher.conftest import TEACHER, TEACHER2, TEACHER_ID

BAD_INVARIANTS = (
    [
        ((FULL_NAME_MAX_LENGTH + 1) * "a", None, TeacherFullNameError),
    ],
)


def test_create_teacher(
    create_teacher: CreateTeacher,
    transaction_manager: MockedTransactionManager,
    teacher_gateway: MockedTeacherGateway,
) -> None:
    data = NewTeacher(
        full_name="John Doe",
        avatar=None,
    )

    create_teacher.execute(data)

    assert transaction_manager.is_begin
    assert transaction_manager.is_commited
    assert teacher_gateway.is_wrote


@pytest.mark.parametrize(
    ("full_name", "avatar", "exc_class"),
    *BAD_INVARIANTS,
)
def test_create_teacher_bad_invariants(
    create_teacher: CreateTeacher,
    full_name: str,
    avatar: str | None,
    exc_class: type[ApplicationError],
) -> None:
    data = NewTeacher(
        avatar=avatar,
        full_name=full_name,
    )

    with pytest.raises(exc_class):
        create_teacher.execute(data)


def test_read_teacher(
    read_teacher: ReadTeacher,
    teacher_gateway: MockedTeacherGateway,
) -> None:
    teacher_gateway.write_teacher(TEACHER)
    teacher = read_teacher.execute(TEACHER_ID)

    assert teacher.teacher_id == TEACHER_ID


def test_read_teachers(
    read_teachers: ReadTeachers,
    teacher_gateway: MockedTeacherGateway,
) -> None:
    teacher_gateway.write_teacher(TEACHER)
    teacher_gateway.write_teacher(TEACHER2)
    teachers: TeachersReadModel = read_teachers.execute()

    assert TEACHER in teachers.teachers
    assert TEACHER2 in teachers.teachers


def test_update_teacher(
    update_teacher: UpdateTeacher,
    teacher_gateway: MockedTeacherGateway,
    transaction_manager: MockedTransactionManager,
) -> None:
    teacher_gateway.write_teacher(TEACHER)

    updated_id = update_teacher.execute(
        UpdatedTeacher(
            teacher_id=TEACHER_ID,
            avatar=TEACHER.avatar,
            full_name=TEACHER.full_name,
        ),
    )

    assert teacher_gateway.is_updated
    assert transaction_manager.is_begin
    assert transaction_manager.is_commited
    assert updated_id == TEACHER_ID


@pytest.mark.parametrize(
    ("full_name", "avatar", "exc_class"),
    *BAD_INVARIANTS,
)
def test_update_teacher_bad_invariants(
    teacher_gateway: MockedTeacherGateway,
    update_teacher: UpdateTeacher,
    full_name: str,
    avatar: str | None,
    exc_class: type[ApplicationError],
) -> None:
    teacher_gateway.write_teacher(TEACHER)

    with pytest.raises(exc_class):
        update_teacher.execute(
            UpdatedTeacher(
                teacher_id=TEACHER_ID,
                avatar=avatar,
                full_name=full_name,
            ),
        )


def test_delete_teacher(
    delete_teacher: DeleteTeacher,
    teacher_gateway: MockedTeacherGateway,
    transaction_manager: MockedTransactionManager,
) -> None:
    teacher_gateway.write_teacher(TEACHER)
    delete_teacher.execute(TEACHER_ID)

    assert transaction_manager.is_begin
    assert transaction_manager.is_commited
    assert teacher_gateway.is_deleted
