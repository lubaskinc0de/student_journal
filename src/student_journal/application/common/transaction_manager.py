from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import Protocol


class TransactionManager(Protocol):
    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...

    @abstractmethod
    def begin(self) -> AbstractContextManager[None]: ...
