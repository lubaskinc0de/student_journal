from sqlite3 import Cursor

import pytest
from student_journal.adapters.db.gateway.student_gateway import SQLiteStudentGateway


@pytest.fixture()
def student_gateway(cursor: Cursor) -> SQLiteStudentGateway:
    return SQLiteStudentGateway(cursor)
