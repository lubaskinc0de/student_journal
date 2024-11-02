from sqlite3 import Cursor

import pytest
from student_journal.adapters.db.gateway.teacher_gateway import SQLiteTeacherGateway


@pytest.fixture()
def teacher_gateway(cursor: Cursor) -> SQLiteTeacherGateway:
    return SQLiteTeacherGateway(cursor)
