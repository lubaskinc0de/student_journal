from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.exceptions.student import StudentDoesNotExistError
from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


class MockedStudentGateway(StudentGateway):
    AVG_MARK = 4.5

    def __init__(self) -> None:
        self._students = {}
        self.is_updated = False
        self.is_wrote = False

    def read_student(self, student_id: StudentId) -> Student:
        if not (student := self._students.get(student_id)):
            raise StudentDoesNotExistError

        return student

    def write_student(self, student: Student) -> None:
        self.is_wrote = True
        self._students[student.student_id] = student

    def get_overall_avg_mark(self) -> float:
        return self.AVG_MARK

    def update_student(self, student: Student) -> None:
        self.is_updated = True
        self.write_student(student)
