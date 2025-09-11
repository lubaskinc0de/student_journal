import tomllib
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

import structlog
import tomli_w

from student_journal.application.common.id_provider import StudentIdProvider
from student_journal.application.common.logger import Logger
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.exceptions.student import (
    StudentIsNotAuthenticatedError,
    StudentNotFoundError,
)
from student_journal.domain.id_type.student_id import StudentId

logger: Logger = structlog.get_logger(__name__)


@dataclass(slots=True, frozen=True)
class CredentialsConfig:
    path: Path


@dataclass(slots=True, frozen=True)
class SimpleStudentIdProvider(StudentIdProvider):
    student_id: StudentId

    def get_student_id(self) -> StudentId:
        return self.student_id

    def require_auth(self) -> None: ...


@dataclass(slots=True, frozen=True)
class FileStudentIdProvider(StudentIdProvider):
    config: CredentialsConfig
    gateway: StudentGateway

    def get_student_id(self) -> StudentId:
        if not self.config.path.exists() or not self.config.path.is_file():
            logger.warning("Credentials file not found", config_path=self.config.path)
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
                logger.warning("Failed to authenticate student with file system.")
                raise StudentIsNotAuthenticatedError from e
            else:
                logger.debug(
                    "Successfully authenticated student",
                    student_id=student_id,
                )
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
        logger.debug("Saved student creds to file system", student_id=student_id)

    def require_auth(self) -> None:
        self.get_student_id()
