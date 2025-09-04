from abc import abstractmethod
from datetime import timezone
from typing import Protocol


class TimezoneProvider(Protocol):
    @abstractmethod
    def get_timezone(self) -> timezone:
        raise NotImplementedError
