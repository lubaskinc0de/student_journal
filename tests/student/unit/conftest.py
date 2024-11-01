import pytest
from common.mock.transaction_manager import MockedTransactionManager

from student.unit.mock.student_gateway import MockedStudentGateway


@pytest.fixture()
def transaction_manager() -> MockedTransactionManager:
    return MockedTransactionManager()


@pytest.fixture()
def student_gateway() -> MockedStudentGateway:
    return MockedStudentGateway()
