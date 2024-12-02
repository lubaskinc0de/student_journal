import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from dataclasses import dataclass
from sqlite3 import Connection

from student_journal.adapters.db.connection_maker import SQLiteConnectionMaker


@dataclass(slots=True, frozen=True)
class SQLiteConnectionFactory:
    connection_maker: SQLiteConnectionMaker

    @contextmanager
    def connection(self) -> Iterator[Connection]:
        conn = self.connection_maker.create_connection()
        conn.row_factory = sqlite3.Row

        with closing(conn) as c:
            c.execute("PRAGMA foreign_keys = ON;")
            yield c
