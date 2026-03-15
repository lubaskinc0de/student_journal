from typing import Generic, TypeVar

T = TypeVar("T")


class StudentAccessService(Generic[T]):
    def ensure_has_access(self, obj: T) -> None: ...
