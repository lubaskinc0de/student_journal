import os
from pathlib import Path
from sqlite3 import Cursor

PATH = Path(
    os.path.join(  # noqa: PTH118
        os.path.dirname(os.path.abspath(__file__)),  # noqa: PTH100, PTH120
        "schema.sql",
    ),
)


def load_and_execute(cursor: Cursor) -> None:
    with PATH.open() as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
