from dataclasses import dataclass
from sqlite3 import Cursor

from student_journal.adapters.models import (
    teacher_retort,
    teacher_to_list_retort,
)
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.application.exceptions.teacher import (
    TeacherDoesNotExistError,
)
from student_journal.domain.teacher import Teacher
from student_journal.domain.value_object.teacher_id import TeacherId


@dataclass(slots=True, frozen=True)
class SQLiteTeacherGateway(TeacherGateway):
    cursor: Cursor

    def read_teacher(self, teacher_id: TeacherId) -> Teacher:
        query = """
            SELECT teacher_id, full_name, avatar
            FROM Teacher WHERE teacher_id = ?
            """
        res = self.cursor.execute(query, (str(teacher_id),)).fetchone()

        if not res:
            raise TeacherDoesNotExistError

        teacher = teacher_retort.load(res, Teacher)

        return teacher

    def write_teacher(self, teacher: Teacher) -> None:
        query = """
            INSERT INTO Teacher
            (teacher_id, full_name, avatar)
            VALUES (?, ?, ?)
            """
        params = teacher_to_list_retort.dump(teacher)
        self.cursor.execute(query, params)

    def read_teachers(self) -> list[Teacher]:
        query = """
            SELECT teacher_id, full_name, avatar
            FROM Teacher
            """
        res = self.cursor.execute(query).fetchall()

        teachers = teacher_retort.load(res, list[Teacher])

        return teachers

    def update_teacher(self, teacher: Teacher) -> None:
        query = """
            UPDATE Teacher
            SET full_name = ?, avatar = ?
            WHERE teacher_id = ?
            """
        params = teacher_to_list_retort.dump(teacher)
        params.append(params.pop(0))

        self.cursor.execute(query, params)

    def delete_teacher(self, teacher_id: TeacherId) -> None:
        query = """
            DELETE FROM Teacher
            WHERE teacher_id = ?
            """

        self.cursor.execute(query, (str(teacher_id),))
