from student_journal.application.exceptions.home_task import (
    HomeTaskDescriptionError,
)

DESCRIPTION_MAX_LENGTH = 65535
DESCRIPTION_MIN_LENGTH = 1


def validate_home_task_invariants(
    description: str,
) -> None:
    if len(description) > DESCRIPTION_MAX_LENGTH:
        raise HomeTaskDescriptionError

    if len(description) < DESCRIPTION_MIN_LENGTH:
        raise HomeTaskDescriptionError
