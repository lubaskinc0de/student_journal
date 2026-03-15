from collections.abc import Iterable
from sqlite3 import Connection, Cursor

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

from student_journal.adapters.db.gateway.student_gateway import SQLiteStudentGateway
from student_journal.adapters.db.migrations.config import get_alembic_config_path


@pytest.fixture
def connection() -> Iterable[Connection]:
    """Override the base connection fixture without pre-inserting a student."""
    engine = create_engine("sqlite:///:memory:")

    with engine.connect() as sa_conn:
        alembic_path_gen = get_alembic_config_path()
        alembic_path = str(next(alembic_path_gen))

        cfg = Config(alembic_path)
        cfg.attributes["connection"] = sa_conn
        command.upgrade(cfg, "head")

        raw_conn = sa_conn.connection.dbapi_connection
        raw_conn.row_factory = __import__("sqlite3").Row

        yield raw_conn


@pytest.fixture
def student_gateway(cursor: Cursor) -> SQLiteStudentGateway:
    return SQLiteStudentGateway(cursor)
