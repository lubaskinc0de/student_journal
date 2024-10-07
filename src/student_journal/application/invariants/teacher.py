from student_journal.application.exceptions.teacher import TeacherFullNameError

FULL_NAME_MAX_LENGTH = 255


def validate_teacher_invariants(full_name: str) -> None:
    if len(full_name) > FULL_NAME_MAX_LENGTH:
        raise TeacherFullNameError
