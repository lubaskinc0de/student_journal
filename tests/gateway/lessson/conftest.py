from sqlite3 import Cursor

import pytest

from student_journal.adapters.db.gateway.lesson_gateway import SQLiteLessonGateway


@pytest.fixture
def lesson_gateway(cursor: Cursor) -> SQLiteLessonGateway:
    return SQLiteLessonGateway(cursor)
