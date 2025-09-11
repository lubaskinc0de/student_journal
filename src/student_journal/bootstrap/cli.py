import argparse

from student_journal.adapters.db.migrations.scripts import new_migration, run_migrations
from student_journal.bootstrap.entrypoint.qt import main as qt_main


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
