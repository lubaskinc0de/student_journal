from uuid import uuid4

import pytest
from common.mock.transaction_manager import MockedTransactionManager

from student_journal.adapters.id_provider import SimpleIdProvider
from student_journal.application.common.id_provider import IdProvider
from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId

STUDENT_ID = StudentId(uuid4())
STUDENT = Student(
    student_id=STUDENT_ID,
    age=14,
    avatar=None,
    name="Ilya",
    home_address=None,
)


@pytest.fixture
def idp() -> IdProvider:
    return SimpleIdProvider(STUDENT_ID)


@pytest.fixture
def transaction_manager() -> MockedTransactionManager:
    return MockedTransactionManager()
