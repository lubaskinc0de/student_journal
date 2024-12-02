from student_journal.application.exceptions.subject import SubjectTitleError

TITLE_MAX_LENGTH = 255
TITLE_MIN_LENGTH = 1


def validate_subject_invariants(title: str) -> None:
    if (len(title) > TITLE_MAX_LENGTH) or (len(title) < TITLE_MIN_LENGTH):
        raise SubjectTitleError
