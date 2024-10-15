from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.exceptions.teacher import TeacherDoesNotExistError
from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.teacher_id import TeacherId


class MockedTeacherGateway(TeacherGateway):
    def __init__(self) -> None:
        self._teachers = {}
        self.is_updated = False
        self.is_wrote = False
        self.is_deleted = False

    def read_teacher(self, teacher_id: TeacherId) -> Teacher:
        if not (teacher := self._teachers.get(teacher_id)):
            raise TeacherDoesNotExistError

        return teacher

    def write_teacher(self, teacher: Teacher) -> None:
        self.is_wrote = True
        self._teachers[teacher.teacher_id] = teacher

    def read_teachers(self) -> list[Teacher]:
        return list(self._teachers.values())

    def update_teacher(self, teacher: Teacher) -> None:
        self.is_updated = True
        self.write_teacher(teacher)

    def delete_teacher(self, teacher_id: TeacherId) -> None:
        del self._teachers[teacher_id]
        self.is_deleted = True
