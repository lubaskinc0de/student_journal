import argparse
import contextlib

import alembic.config

from student_journal.adapters.db.migrations.config import get_alembic_config_path
from student_journal.bootstrap.entrypoint.qt import main as qt_main


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Student Journal Application")

    parser.add_argument("module", nargs="?", help="module to use (e.g., run)")
    parser.add_argument("option", nargs="?", help="option to execute (e.g., gui)")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="additional arguments")

    args = parser.parse_args()

    if not args.module or not args.option:
        parser.print_help()
        return

    modules = {
        "run": {
            "gui": qt_main,
        },
        "migrations": {
            "new": new_migration,
            "run": run_migrations,
        },
    }

    if args.module in modules and args.option in modules[args.module]:  # type: ignore
        modules[args.module][args.option](args.args)  # type: ignore
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
