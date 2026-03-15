import contextlib

import alembic.config

from student_journal.adapters.db.migrations.config import get_alembic_config_path


def new_migration(args: list[str]) -> None:
    alembic_path_gen = get_alembic_config_path()
    alembic_path = str(next(alembic_path_gen))
    alembic.config.main(argv=["-c", alembic_path, "revision", "-m", " ".join(args)])
    with contextlib.suppress(StopIteration):
        next(alembic_path_gen)


def run_migrations(_args: list[str]) -> None:
    alembic_path_gen = get_alembic_config_path()
    alembic_path = str(next(alembic_path_gen))
    alembic.config.main(argv=["-c", alembic_path, "upgrade", "head"])
    with contextlib.suppress(StopIteration):
        next(alembic_path_gen)
