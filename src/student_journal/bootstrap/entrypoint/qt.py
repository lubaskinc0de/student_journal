import logging

from PyQt6.QtGui import QIcon

import student_journal.presentation.resource

from importlib.resources import as_file, files

import signal
import sys
from functools import partial
from types import TracebackType

from PyQt6.QtWidgets import QApplication, QMessageBox

import student_journal
from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.exceptions.base import ApplicationError
from student_journal.application.exceptions.student import (
    StudentIsNotAuthenticatedError,
)
from student_journal.bootstrap.di.container import get_container_for_gui
from student_journal.presentation.widget.main_window import MainWindow

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def display_error_text(wnd: MainWindow, text: str) -> None:
    msg = QMessageBox(wnd)
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Ошибка приложения")
    msg.setText("Произошла ошибка!")
    msg.setInformativeText(text)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def except_hook(
    app: QApplication,
    error_locator: ErrorLocator,
    wnd: MainWindow,
    _exc_type: type[Exception],
    exc_value: BaseException,
    _exc_traceback: TracebackType,
) -> None:
    match exc_value:
        case StudentIsNotAuthenticatedError() as e:
            text = error_locator.get_text(e)
            display_error_text(wnd, text)
            app.closeAllWindows()
            wnd.show()
            wnd.display_register()

        case ApplicationError() as e:
            text = error_locator.get_text(e)
            display_error_text(wnd, text)

        case BaseException() as e:
            logging.critical("Unhandled exception", exc_info=e)
            sys.exit()


def main(_argv: list[str]) -> None:
    container = get_container_for_gui()
    resources = files(student_journal.presentation.resource)

    app = QApplication(_argv)

    main_wnd = MainWindow(container)
    main_wnd.setWindowTitle("Дневник Школьника")

    with as_file(resources.joinpath("styles.qss")) as qss_path:
        app.setStyleSheet(qss_path.read_text())

    main_wnd.show()

    locator = container.get(ErrorLocator)
    sys.excepthook = partial(except_hook, app, locator, main_wnd)

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec())


if __name__ == "__main__":
    main(sys.argv)
