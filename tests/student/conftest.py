from uuid import uuid4

import pytest
from student_journal.adapters.id_provider import SimpleIdProvider
from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.student.create_student import CreateStudent
from student_journal.application.student.read_student import ReadStudent
from student_journal.application.student.update_student import UpdateStudent
from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


@pytest.fixture()
def idp() -> IdProvider:
    return SimpleIdProvider(STUDENT_ID)


@pytest.fixture()
def create_student(
    transaction_manager: TransactionManager,
    student_gateway: StudentGateway,
) -> CreateStudent:
    return CreateStudent(
        transaction_manager=transaction_manager,
        gateway=student_gateway,
    )


@pytest.fixture()
def read_student(
    student_gateway: StudentGateway,
    idp: IdProvider,
) -> ReadStudent:
    return ReadStudent(
        gateway=student_gateway,
        idp=idp,
    )


@pytest.fixture()
def update_student(
    student_gateway: StudentGateway,
    idp: IdProvider,
    transaction_manager: TransactionManager,
) -> UpdateStudent:
    return UpdateStudent(
        gateway=student_gateway,
        idp=idp,
        transaction_manager=transaction_manager,
    )


STUDENT_ID = StudentId(uuid4())
STUDENT = Student(
    student_id=STUDENT_ID,
    age=14,
    avatar=None,
    name="Ilya",
    home_address=None,
)
