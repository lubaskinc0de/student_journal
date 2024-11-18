from abc import abstractmethod
from typing import Protocol

from student_journal.application.exceptions.base import ApplicationError


class ErrorLocator(Protocol):
    @abstractmethod
    def get_text(self, error: ApplicationError) -> str: ...
