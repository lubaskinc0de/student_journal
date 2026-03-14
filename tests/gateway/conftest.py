from collections.abc import Iterable
from sqlite3 import Connection, Cursor

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from unit.conftest import STUDENT_ID

from student_journal.adapters.db.migrations.config import get_alembic_config_path
from student_journal.adapters.db.transaction_manager import SQLiteTransactionManager


@pytest.fixture
def connection() -> Iterable[Connection]:
    engine = create_engine("sqlite:///:memory:")

    with engine.connect() as sa_conn:
        alembic_path_gen = get_alembic_config_path()
        alembic_path = str(next(alembic_path_gen))

        cfg = Config(alembic_path)
        cfg.attributes["connection"] = sa_conn
        command.upgrade(cfg, "head")

        raw_conn = sa_conn.connection.dbapi_connection
        raw_conn.row_factory = __import__("sqlite3").Row

        # Insert the test student for FK constraints
        raw_conn.execute(
            "INSERT INTO Student (student_id, age, name) VALUES (?, ?, ?)",
            (str(STUDENT_ID), 14, "Test"),
        )

        yield raw_conn


@pytest.fixture
def cursor(connection: Connection) -> Cursor:
    return connection.cursor()


@pytest.fixture
def transaction_manager(connection: Connection) -> SQLiteTransactionManager:
    return SQLiteTransactionManager(connection)
