from importlib.resources import as_file, files
from sqlite3 import Cursor

import student_journal.adapters.db.schema


def load_and_execute(cursor: Cursor) -> None:
    source = files(student_journal.adapters.db.schema).joinpath("schema.sql")

    with as_file(source) as sql_path, sql_path.open() as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)
