import sys
from functools import partial
from types import TracebackType

from PyQt6.QtWidgets import QApplication, QMessageBox

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.exceptions.base import ApplicationError
from student_journal.bootstrap.di.container import get_container_for_gui
from student_journal.presentation.widget.main_window import MainWindow


def except_hook(
    error_locator: ErrorLocator,
    wnd: MainWindow,
    _exc_type: type[Exception],
    exc_value: Exception,
    _exc_traceback: TracebackType,
) -> None:
    match exc_value:
        case ApplicationError() as e:
            msg = QMessageBox(wnd)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Ошибка приложения")
            msg.setText("Произошла ошибка!")
            msg.setInformativeText(error_locator.get_text(e))
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        case _:
            sys.exit()


def main(_argv: list[str]) -> None:
    container = get_container_for_gui()

    app = QApplication(_argv)
    main_wnd = MainWindow(container)
    main_wnd.show()

    locator = container.get(ErrorLocator)
    sys.excepthook = partial(except_hook, locator, main_wnd)

    sys.exit(app.exec())
