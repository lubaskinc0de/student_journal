import sys

from student_journal.bootstrap.entrypoint.qt import main as qt_main


def main() -> None:
    argv = sys.argv[1:]

    if not argv:
        return

    try:
        module = argv[0]
        option = argv[1]
        args = argv[2:]
    except IndexError:
        return

    modules = {
        "run": {
            "gui": qt_main,
        },
    }

    if module not in modules:
        return

    if option not in modules[module]:
        return

    modules[module][option](args)
