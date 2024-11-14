from sqlite3 import Cursor

import pytest
from unit.conftest import HOME_TASK, HOME_TASK_2, LESSON_ID, TASK_ID

from student_journal.adapters.models.home_task import (
    home_task_retort,
)
from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.exceptions.home_task import HomeTaskDoesNotExistError
from student_journal.domain.home_task import HomeTask

READ_HOME_TASK_SQL = "SELECT * FROM Hometask"


def test_write(
    home_task_gateway: HomeTaskGateway,
    cursor: Cursor,
) -> None:
    home_task_gateway.write_home_task(HOME_TASK)
    db_home_task = home_task_retort.load(
        dict(cursor.execute(READ_HOME_TASK_SQL).fetchone()),
        HomeTask,
    )
    assert db_home_task == HOME_TASK


def test_read(
    home_task_gateway: HomeTaskGateway,
    cursor: Cursor,
) -> None:
    home_task_gateway.write_home_task(HOME_TASK)
    db_home_task = home_task_retort.load(
        dict(cursor.execute(READ_HOME_TASK_SQL).fetchone()),
        HomeTask,
    )

    assert db_home_task == home_task_gateway.read_home_task(TASK_ID)


def test_read_not_exist(
    home_task_gateway: HomeTaskGateway,
) -> None:
    with pytest.raises(HomeTaskDoesNotExistError):
        home_task_gateway.read_home_task(TASK_ID)


def test_read_home_tasks(
    home_task_gateway: HomeTaskGateway,
    cursor: Cursor,
) -> None:
    home_task_gateway.write_home_task(HOME_TASK)
    home_task_gateway.write_home_task(HOME_TASK_2)

    home_tasks_list = [
        dict(home_task) for home_task in cursor.execute(READ_HOME_TASK_SQL).fetchall()
    ]

    db_home_tasks = home_task_retort.load(
        home_tasks_list,
        list[HomeTask],
    )

    for home_task in db_home_tasks:
        home_task.is_done = bool(home_task.is_done)

    assert db_home_tasks == home_task_gateway.read_home_tasks()


def test_update(
    home_task_gateway: HomeTaskGateway,
    cursor: Cursor,
) -> None:
    home_task_gateway.write_home_task(HOME_TASK)
    updated_home_task = HomeTask(
        task_id=TASK_ID,
        lesson_id=LESSON_ID,
        description="testtest22222",
        is_done=True,
    )

    home_task_gateway.update_home_task(updated_home_task)
    home_task_dict = dict(cursor.execute(READ_HOME_TASK_SQL).fetchone())
    home_task_dict["is_done"] = bool(home_task_dict["is_done"])
    db_home_task = home_task_retort.load(
        home_task_dict,
        HomeTask,
    )
    assert db_home_task == updated_home_task
