from datetime import datetime
from uuid import uuid4

import pytest
from common.mock.transaction_manager import MockedTransactionManager

from student_journal.adapters.id_provider import SimpleIdProvider
from student_journal.application.common.id_provider import IdProvider
from student_journal.domain.lesson import Lesson
from student_journal.domain.student import Student
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.student_id import StudentId
from student_journal.domain.value_object.subject_id import SubjectId

STUDENT_ID = StudentId(uuid4())
STUDENT = Student(
    student_id=STUDENT_ID,
    age=14,
    avatar=None,
    name="Ilya",
    home_address=None,
)

SUBJECT_ID = SubjectId(uuid4())
LESSON_ID = LessonId(uuid4())
LESSON = Lesson(
    lesson_id=LESSON_ID,
    subject_id=SUBJECT_ID,
    at=datetime(2024, 11, 15),
    mark=None,
    note=None,
    room=5,
    index_number=3,
)
LESSON_MONDAY_ID = LessonId(uuid4())
LESSON_MONDAY = Lesson(
    lesson_id=LESSON_MONDAY_ID,
    subject_id=SUBJECT_ID,
    at=datetime(2024, 11, 11),
    mark=None,
    note=None,
    room=5,
    index_number=3,
)
LESSON_MONDAY_2_ID = LessonId(uuid4())
LESSON_MONDAY_2 = Lesson(
    lesson_id=LESSON_MONDAY_2_ID,
    subject_id=SUBJECT_ID,
    at=datetime(2024, 11, 18),
    mark=None,
    note=None,
    room=5,
    index_number=3,
)


@pytest.fixture
def idp() -> IdProvider:
    return SimpleIdProvider(STUDENT_ID)


@pytest.fixture
def transaction_manager() -> MockedTransactionManager:
    return MockedTransactionManager()
