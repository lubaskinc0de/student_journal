from sqlite3 import Cursor

import pytest

from student_journal.adapters.db.gateway.home_task_gateway import SQLiteHomeTaskGateway


@pytest.fixture
def home_task_gateway(cursor: Cursor) -> SQLiteHomeTaskGateway:
    return SQLiteHomeTaskGateway(cursor)
