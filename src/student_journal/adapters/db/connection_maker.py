import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection


@dataclass(slots=True, frozen=True)
class SQLiteConnectionMaker:
    database: str

    def create_connection(self) -> Connection:
        return sqlite3.connect(self.database)
