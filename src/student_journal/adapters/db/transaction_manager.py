from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from sqlite3 import Connection

from student_journal.application.common.transaction_manager import TransactionManager


@dataclass(slots=True, frozen=True)
class SQLiteTransactionManager(TransactionManager):
    connection: Connection

    @contextmanager
    def begin(self) -> Iterator[None]:
        yield None

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()
