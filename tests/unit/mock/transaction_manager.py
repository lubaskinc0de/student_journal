from student_journal.application.common.transaction_manager import TransactionManager


class MockedTransactionManager(TransactionManager):
    def __init__(self) -> None:
        self.is_commited = False
        self.is_rolled_back = False
        self.is_begin = False

    def begin(self) -> None:
        if self.is_begin:
            raise ValueError("Transaction tries to begin twice!")
        self.is_begin = True

    def commit(self) -> None:
        if self.is_commited:
            raise ValueError("Transaction tries to commit twice!")

        if not self.is_begin:
            raise ValueError("Transaction is not begin!")

        self.is_commited = True

    def rollback(self) -> None:
        if not self.is_begin:
            raise ValueError("Transaction is not begin!")

        if self.is_rolled_back:
            raise ValueError("Transaction tries to rollback twice!")

        self.is_rolled_back = True
