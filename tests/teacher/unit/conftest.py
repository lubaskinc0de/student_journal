from uuid import uuid4

import pytest
from student.unit.mock import MockedTeacherGateway, MockedTransactionManager
from student_journal.adapters.id_provider import SimpleIdProvider
from student_journal.application.common.id_provider import IdProvider
from student_journal.application.teacher import (
    CreateTeacher,
    DeleteTeacher,
    ReadTeacher,
    ReadTeachers,
    UpdateTeacher,
)
from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.student_id import StudentId
from student_journal.domain.value_object.teacher_id import TeacherId

TEACHER_ID = TeacherId(uuid4())
TEACHER = Teacher(
    teacher_id=TEACHER_ID,
    full_name="John Doe",
    avatar=None,
)

TEACHER2_ID = TeacherId(uuid4())
TEACHER2 = Teacher(
    teacher_id=TEACHER2_ID,
    full_name="John Not Doe",
    avatar=None,
)
STUDENT_ID = StudentId(uuid4())


@pytest.fixture()
def idp() -> IdProvider:
    return SimpleIdProvider(STUDENT_ID)


@pytest.fixture()
def transaction_manager() -> MockedTransactionManager:
    return MockedTransactionManager()


@pytest.fixture()
def teacher_gateway() -> MockedTeacherGateway:
    return MockedTeacherGateway()


@pytest.fixture()
def create_teacher(
    transaction_manager: MockedTransactionManager,
    teacher_gateway: MockedTeacherGateway,
) -> CreateTeacher:
    return CreateTeacher(
        transaction_manager=transaction_manager,
        gateway=teacher_gateway,
    )


@pytest.fixture()
def read_teacher(
    teacher_gateway: MockedTeacherGateway,
) -> ReadTeacher:
    return ReadTeacher(
        gateway=teacher_gateway,
    )


@pytest.fixture()
def update_teacher(
    teacher_gateway: MockedTeacherGateway,
    transaction_manager: MockedTransactionManager,
) -> UpdateTeacher:
    return UpdateTeacher(
        gateway=teacher_gateway,
        transaction_manager=transaction_manager,
    )


@pytest.fixture()
def read_teachers(
    teacher_gateway: MockedTeacherGateway,
    idp: IdProvider,
) -> ReadTeachers:
    return ReadTeachers(
        idp=idp,
        gateway=teacher_gateway,
    )


@pytest.fixture()
def delete_teacher(
    teacher_gateway: MockedTeacherGateway,
    transaction_manager: MockedTransactionManager,
) -> DeleteTeacher:
    return DeleteTeacher(
        transaction_manager=transaction_manager,
        gateway=teacher_gateway,
    )
