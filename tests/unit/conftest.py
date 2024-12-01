from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from common.mock.transaction_manager import MockedTransactionManager

from student_journal.adapters.id_provider import SimpleIdProvider
from student_journal.application.common.id_provider import IdProvider
from student_journal.domain.home_task import HomeTask
from student_journal.domain.lesson import Lesson
from student_journal.domain.student import Student
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.student_id import StudentId
from student_journal.domain.value_object.subject_id import SubjectId
from student_journal.domain.value_object.task_id import HomeTaskId

student_timezone = timezone(timedelta(hours=3))
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
    at=datetime(2024, 11, 15, tzinfo=student_timezone),
    mark=None,
    note=None,
    room=5,
    index_number=3,
)

LESSON_MONDAY_ID = LessonId(uuid4())
LESSON_MONDAY = Lesson(
    lesson_id=LESSON_MONDAY_ID,
    subject_id=SUBJECT_ID,
    at=datetime(2024, 11, 11, hour=8, minute=0, tzinfo=student_timezone),
    mark=None,
    note=None,
    room=5,
    index_number=3,
)

LESSON_WEDNESDAY_ID = LessonId(uuid4())
LESSON_WEDNESDAY = Lesson(
    lesson_id=LESSON_WEDNESDAY_ID,
    subject_id=SUBJECT_ID,
    at=datetime(2024, 11, 13, hour=8, minute=0, tzinfo=student_timezone),
    mark=None,
    note=None,
    room=5,
    index_number=3,
)

LESSON_MONDAY_2_ID = LessonId(uuid4())
LESSON_MONDAY_2 = Lesson(
    lesson_id=LESSON_MONDAY_2_ID,
    subject_id=SUBJECT_ID,
    at=datetime(2024, 11, 19, tzinfo=student_timezone),
    mark=None,
    note=None,
    room=5,
    index_number=3,
)

TASK_ID = HomeTaskId(uuid4())
HOME_TASK = HomeTask(
    task_id=TASK_ID,
    lesson_id=LESSON_ID,
    description="§13 упр 13",
    is_done=False,
)

TASK_ID_2 = HomeTaskId(uuid4())
HOME_TASK_2 = HomeTask(
    task_id=TASK_ID_2,
    lesson_id=LESSON_MONDAY_2_ID,
    description="§12 упр 12",
    is_done=True,
)


@pytest.fixture
def idp() -> IdProvider:
    return SimpleIdProvider(STUDENT_ID)


@pytest.fixture
def transaction_manager() -> MockedTransactionManager:
    return MockedTransactionManager()
