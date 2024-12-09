import tomllib
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

import tomli_w

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.exceptions.student import (
    StudentIsNotAuthenticatedError,
    StudentNotFoundError,
)
from student_journal.domain.id_type.student_id import StudentId


@dataclass(slots=True, frozen=True)
class CredentialsConfig:
    path: Path


@dataclass(slots=True, frozen=True)
class SimpleStudentIdProvider(StudentIdProvider):
    student_id: StudentId

    def get_id(self) -> StudentId:
        return self.student_id

    def ensure_auth(self) -> None: ...


@dataclass(slots=True, frozen=True)
class FileStudentIdProvider(StudentIdProvider):
    config: CredentialsConfig
    gateway: StudentGateway

    def get_id(self) -> StudentId:
        if not self.config.path.exists() or not self.config.path.is_file():
            raise StudentIsNotAuthenticatedError from FileNotFoundError

        with self.config.path.open("rb") as f:
            try:
                data = tomllib.load(f)
                student_id = StudentId(UUID(data["auth"]["student_id"]))
                self.gateway.read_student(student_id)
            except (
                ValueError,
                tomllib.TOMLDecodeError,
                KeyError,
                StudentNotFoundError,
            ) as e:
                raise StudentIsNotAuthenticatedError from e
            else:
                return student_id

    def save(self, student_id: StudentId) -> None:
        with self.config.path.open("wb") as f:
            tomli_w.dump(
                {
                    "auth": {
                        "student_id": student_id.hex,
                    },
                },
                f,
            )

    def ensure_auth(self) -> None:
        self.get_id()
