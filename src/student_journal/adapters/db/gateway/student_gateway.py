from dataclasses import dataclass
from sqlite3 import Cursor

from student_journal.adapters.converter.student import (
    student_retort,
    student_to_list_retort,
)
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.exceptions.student import StudentDoesNotExistError
from student_journal.domain.student import Student
from student_journal.domain.value_object.student_id import StudentId


@dataclass(slots=True, frozen=True)
class SQLiteStudentGateway(StudentGateway):
    cursor: Cursor

    def read_student(self, student_id: StudentId) -> Student:
        query = (
            "SELECT student_id, age, avatar, name, home_address, timezone "
            "FROM Student WHERE student_id = ?"
        )
        res = self.cursor.execute(query, (str(student_id),)).fetchone()

        if not res:
            raise StudentDoesNotExistError

        student = student_retort.load(res, Student)

        return student

    def write_student(self, student: Student) -> None:
        query = (
            "INSERT INTO Student "
            "(student_id, age, avatar, name, home_address, timezone) "
            "VALUES "
            "(?, ?, ?, ?, ?, ?)"
        )
        params = student_to_list_retort.dump(student)
        self.cursor.execute(query, params)

    def update_student(self, student: Student) -> None:
        query = (
            "UPDATE Student "
            "SET age = ?, avatar = ?, name = ?, home_address = ?, timezone = ? "
            "WHERE student_id = ?"
        )
        params = student_to_list_retort.dump(student)
        params.append(params.pop(0))

        self.cursor.execute(query, params)

    def get_overall_avg_mark(self) -> float:
        query = "SELECT avg(mark) FROM Lessons"
        res = self.cursor.execute(query).fetchone()

        if not res or not res[0]:
            return 0.0

        return res[0]  # type: ignore
