from collections.abc import Iterable
from sqlite3 import Connection, Cursor

from dishka import Provider, Scope, provide

from student_journal.adapters.db.connection_factory import SQLiteConnectionFactory
from student_journal.adapters.db.connection_maker import SQLiteConnectionMaker
from student_journal.adapters.db.schema.load_schema import load_and_execute
from student_journal.adapters.db.transaction_manager import SQLiteTransactionManager
from student_journal.application.common.transaction_manager import TransactionManager


class DbProvider(Provider):
    scope = Scope.REQUEST

    connection_maker = provide(SQLiteConnectionMaker, scope=Scope.APP)
    transaction_manager = provide(SQLiteTransactionManager, provides=TransactionManager)

    @provide(scope=Scope.APP)
    def connection_factory(
        self,
        maker: SQLiteConnectionMaker,
    ) -> SQLiteConnectionFactory:
        factory = SQLiteConnectionFactory(connection_maker=maker)

        with factory.connection() as conn:
            load_and_execute(conn.cursor())

        return factory

    @provide()
    def connection(self, factory: SQLiteConnectionFactory) -> Iterable[Connection]:
        with factory.connection() as conn:
            yield conn

    @provide()
    def cursor(self, conn: Connection) -> Cursor:
        return conn.cursor()
