from dataclasses import dataclass
from sqlite3 import Cursor

from student_journal.adapters.converter.subject import (
    subject_retort,
    subject_to_list_retort,
)
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.exceptions.subject import SubjectDoesNotExistError
from student_journal.application.models.subject import SubjectReadModel
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.subject_id import SubjectId


@dataclass(slots=True, frozen=True)
class SQLiteSubjectGateway(SubjectGateway):
    cursor: Cursor

    def read_subject(self, subject_id: SubjectId) -> Subject:
        query = "SELECT subject_id, title, teacher_id FROM Subject WHERE subject_id = ?"
        res = self.cursor.execute(query, (str(subject_id),)).fetchone()

        if not res:
            raise SubjectDoesNotExistError

        subject = subject_retort.load(res, Subject)

        return subject

    def write_subject(self, subject: Subject) -> None:
        query = (
            "INSERT INTO Subject "
            "(subject_id, teacher_id, title) "
            "VALUES "
            "(?, ?, ?)"
        )
        params = subject_to_list_retort.dump(subject)
        self.cursor.execute(query, params)

    def update_subject(self, subject: Subject) -> None:
        query = "UPDATE Subject SET teacher_id = ?, title = ? WHERE subject_id = ?"
        params = subject_to_list_retort.dump(subject)
        params.append(params.pop(0))

        self.cursor.execute(query, params)

    def delete_subject(self, subject_id: SubjectId) -> None:
        query = """DELETE FROM Subject WHERE subject_id = ?"""
        self.cursor.execute(query, (str(subject_id),))

    def read_subjects(self) -> list[SubjectReadModel]:
        query = """
        SELECT
            s.subject_id,
            s.title,
            t.teacher_id,
            t.full_name as teacher_full_name,
            t.avatar as teacher_avatar,
            COALESCE(AVG(l.mark), 0.0) AS avg_mark,
            GROUP_CONCAT(l.mark, '|') AS marks_list
        FROM Subject s
        JOIN Teacher t ON s.teacher_id = t.teacher_id
        LEFT JOIN Lesson l ON s.subject_id = l.subject_id
        GROUP BY s.subject_id
        ORDER BY avg_mark DESC
        """

        res = self.cursor.execute(query).fetchall()
        entries = [dict(x) for x in res]

        for each in entries:
            each["teacher"] = {
                "teacher_id": each["teacher_id"],
                "full_name": each["teacher_full_name"],
                "avatar": each["teacher_avatar"],
            }

            if each["marks_list"] is None:
                each["marks_list"] = []

        result = subject_retort.load(entries, list[SubjectReadModel])
        return result
