from uuid import uuid4

import pytest

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.teacher import (
    CreateTeacher,
    DeleteTeacher,
    ReadTeacher,
    ReadTeachers,
    UpdateTeacher,
)
from student_journal.domain.entity.teacher import Teacher
from student_journal.domain.id_type.teacher_id import TeacherId
from unit.conftest import STUDENT_ID
from unit.student.mock import MockedTeacherGateway, MockedTransactionManager

TEACHER_ID = TeacherId(uuid4())
TEACHER = Teacher(
    teacher_id=TEACHER_ID,
    student_id=STUDENT_ID,
    full_name="John Doe",
    avatar=None,
)
TEACHER2_ID = TeacherId(uuid4())
TEACHER2 = Teacher(
    teacher_id=TEACHER2_ID,
    student_id=STUDENT_ID,
    full_name="John Not Doe",
    avatar=None,
)


@pytest.fixture
def teacher_gateway() -> MockedTeacherGateway:
    return MockedTeacherGateway()


@pytest.fixture
def create_teacher(
    transaction_manager: MockedTransactionManager,
    teacher_gateway: MockedTeacherGateway,
    idp: StudentIdProvider,
) -> CreateTeacher:
    return CreateTeacher(
        transaction_manager=transaction_manager,
        gateway=teacher_gateway,
        idp=idp,
    )


@pytest.fixture
def read_teacher(
    teacher_gateway: MockedTeacherGateway,
    idp: StudentIdProvider,
) -> ReadTeacher:
    return ReadTeacher(
        gateway=teacher_gateway,
        idp=idp,
    )


@pytest.fixture
def update_teacher(
    teacher_gateway: MockedTeacherGateway,
    transaction_manager: MockedTransactionManager,
    idp: StudentIdProvider,
) -> UpdateTeacher:
    return UpdateTeacher(
        gateway=teacher_gateway,
        transaction_manager=transaction_manager,
        idp=idp,
    )


@pytest.fixture
def read_teachers(
    teacher_gateway: MockedTeacherGateway,
    idp: StudentIdProvider,
) -> ReadTeachers:
    return ReadTeachers(
        idp=idp,
        gateway=teacher_gateway,
    )


@pytest.fixture
def delete_teacher(
    teacher_gateway: MockedTeacherGateway,
    transaction_manager: MockedTransactionManager,
    idp: StudentIdProvider,
) -> DeleteTeacher:
    return DeleteTeacher(
        transaction_manager=transaction_manager,
        gateway=teacher_gateway,
        idp=idp,
    )
