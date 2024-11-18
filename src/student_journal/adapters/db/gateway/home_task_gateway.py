from dataclasses import dataclass
from sqlite3 import Cursor

from student_journal.adapters.converter import (
    home_task_retort,
    home_task_to_list_retort,
)
from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.exceptions.home_task import (
    HomeTaskDoesNotExistError,
)
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

        if not res:
            raise HomeTaskDoesNotExistError

        home_task = home_task_retort.load(res, HomeTask)

        return home_task

    def write_home_task(self, home_task: HomeTask) -> None:
        query = """
            INSERT INTO Hometask
            (task_id, lesson_id, description, is_done)
            VALUES (?, ?, ?, ?)
            """
        params = home_task_to_list_retort.dump(home_task)
        self.cursor.execute(query, params)

    def read_home_tasks(self, is_done: bool | None = False) -> list[HomeTask]:
        query = """
            SELECT task_id, lesson_id, description, is_done
            FROM Hometask
            """
        if is_done is not None:
            query += " WHERE is_done = ?"
            res = self.cursor.execute(query, (is_done,)).fetchall()
        else:
            res = self.cursor.execute(query).fetchall()

        home_tasks = home_task_retort.load(res, list[HomeTask])

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
