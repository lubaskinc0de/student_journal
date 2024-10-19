from sqlite3 import Connection, Cursor

import pytest
from student_journal.adapters.db.connection_factory import SQLiteConnectionFactory
from student_journal.adapters.db.connection_maker import SQLiteConnectionMaker
from student_journal.adapters.db.gateway.student_gateway import SQLiteStudentGateway
from student_journal.adapters.db.schema.load_schema import load_and_execute
from student_journal.adapters.db.transaction_manager import SQLiteTransactionManager


@pytest.fixture()
def connection() -> Connection:
    maker = SQLiteConnectionMaker(":memory:")
    factory = SQLiteConnectionFactory(maker)

    with factory.connection() as conn:
        load_and_execute(conn.cursor())
        yield conn


@pytest.fixture()
def cursor(connection: Connection) -> Cursor:
    return connection.cursor()


@pytest.fixture()
def student_gateway(cursor: Cursor) -> SQLiteStudentGateway:
    return SQLiteStudentGateway(cursor)


@pytest.fixture()
def transaction_manager(connection: Connection) -> SQLiteTransactionManager:
    return SQLiteTransactionManager(connection)
