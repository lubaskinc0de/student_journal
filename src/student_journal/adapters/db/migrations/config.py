from collections.abc import Iterator
from importlib.resources import as_file, files
from pathlib import Path

import student_journal.adapters.db


def get_alembic_config_path() -> Iterator[Path]:
    source = files(student_journal.adapters.db).joinpath("alembic.ini")
    with as_file(source) as path:
        yield path
