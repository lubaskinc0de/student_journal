import pytest
from student_journal.application.common.id_provider import IdProvider
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.transaction_manager import TransactionManager
from student_journal.application.student.create_student import CreateStudent
from student_journal.application.student.read_student import ReadStudent
from student_journal.application.student.update_student import UpdateStudent

from unit.student.mock.student_gateway import MockedStudentGateway


@pytest.fixture()
def student_gateway() -> MockedStudentGateway:
    return MockedStudentGateway()


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
