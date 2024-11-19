import sys

from PyQt6.QtWidgets import QApplication

from student_journal.presentation.widget.main_window import MainWindow


def main(_argv: list[str]) -> None:
    app = QApplication(_argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
