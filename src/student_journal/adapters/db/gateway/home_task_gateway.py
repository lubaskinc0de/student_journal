from dataclasses import dataclass
from sqlite3 import Cursor

from student_journal.adapters.converter import (
    home_task_retort,
    home_task_to_list_retort,
)
from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.exceptions.home_task import HomeTaskNotFoundError
from student_journal.application.models.home_task import HomeTaskReadModel
from student_journal.domain.home_task import HomeTask
from student_journal.domain.value_object.task_id import HomeTaskId


@dataclass(slots=True, frozen=True)
class SQLiteHomeTaskGateway(HomeTaskGateway):
    cursor: Cursor

    def read_home_task(self, task_id: HomeTaskId) -> HomeTask:
        query = """
            SELECT task_id, lesson_id, description, is_done
            FROM Hometask WHERE task_id = ?
            """
        res = self.cursor.execute(query, (str(task_id),)).fetchone()

        if res is None:
            raise HomeTaskNotFoundError

        home_task = home_task_retort.load(dict(res), HomeTask)
        return home_task

    def write_home_task(self, home_task: HomeTask) -> None:
        query = """
            INSERT INTO Hometask
            (task_id, lesson_id, description, is_done)
            VALUES (?, ?, ?, ?)
            """
        params = home_task_to_list_retort.dump(home_task)
        self.cursor.execute(query, params)

    def read_home_tasks(self, *, show_done: bool = False) -> list[HomeTaskReadModel]:
        query = """
            SELECT Hometask.task_id, Hometask.description, Hometask.is_done,
            Lesson.lesson_id as lesson_lesson_id,
            Lesson.subject_id as lesson_subject_id,
            Lesson.at as lesson_at,
            Lesson.mark as lesson_mark,
            Lesson.note as lesson_note,
            Lesson.room as lesson_room,
            Subject.subject_id as subject_subject_id,
            Subject.title as subject_title,
            Subject.teacher_id as subject_teacher_id
            FROM Hometask
            JOIN Lesson ON Hometask.lesson_id = Lesson.lesson_id
            JOIN Subject ON Lesson.subject_id = Subject.subject_id
            """
        if show_done is False:
            query += " WHERE is_done = ?"
            res = self.cursor.execute(query, (show_done,)).fetchall()
        else:
            res = self.cursor.execute(query).fetchall()

        rows = [dict(row) for row in res]
        result = []

        for row in rows:
            lesson_fields = [x for x in row if x.startswith("lesson_")]
            subject_fields = [x for x in row if x.startswith("subject_")]
            own_fields = [
                x for x in row if (x not in lesson_fields) and (x not in subject_fields)
            ]
            new_row = {key: row[key] for key in own_fields}
            new_row["lesson"] = {key[7:]: row[key] for key in lesson_fields}
            new_row["subject"] = {key[8:]: row[key] for key in subject_fields}

            result.append(new_row)

        home_tasks = home_task_retort.load(result, list[HomeTaskReadModel])

        return home_tasks

    def update_home_task(self, home_task: HomeTask) -> None:
        query = """
            UPDATE Hometask
            SET lesson_id = ?, description = ?, is_done = ?
            WHERE task_id = ?
            """
        params = home_task_to_list_retort.dump(home_task)

        params.append(params.pop(0))

        self.cursor.execute(query, params)

    def delete_home_task(self, task_id: HomeTaskId) -> None:
        query = """
            DELETE FROM Hometask
            WHERE task_id = ?
            """

        self.cursor.execute(query, (str(task_id),))
