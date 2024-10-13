import pytest
from student_journal.application.student.create_student import CreateStudent

from tests.unit.mock.student_gateway import MockedStudentGateway
from tests.unit.mock.transaction_manager import MockedTransactionManager


@pytest.fixture()
def transaction_manager() -> MockedTransactionManager:
    return MockedTransactionManager()


@pytest.fixture()
def student_gateway() -> MockedStudentGateway:
    return MockedStudentGateway()


@pytest.fixture()
def create_student(
    transaction_manager: MockedTransactionManager,
    student_gateway: MockedStudentGateway,
) -> CreateStudent:
    return CreateStudent(
        transaction_manager=transaction_manager,
        gateway=student_gateway,
    )
