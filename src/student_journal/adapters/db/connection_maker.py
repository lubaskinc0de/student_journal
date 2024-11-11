import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection


@dataclass(slots=True, frozen=True)
class DBConfig:
    db_path: str


@dataclass(slots=True, frozen=True)
class SQLiteConnectionMaker:
    config: DBConfig

    def create_connection(self) -> Connection:
        return sqlite3.connect(self.config.db_path)
