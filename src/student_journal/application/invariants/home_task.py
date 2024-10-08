from student_journal.application.exceptions.home_task import (
    HomeTaskDescriptionError,
)

DESCRIPTION_MAX_LENGTH = 65535


def validate_home_task_invariants(
    description: str,
) -> None:
    if len(description) > DESCRIPTION_MAX_LENGTH:
        raise HomeTaskDescriptionError
