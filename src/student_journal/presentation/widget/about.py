from PyQt6.QtWidgets import QWidget

from student_journal.presentation.ui.about_ui import Ui_About


class About(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_About()
        self.ui.setupUi(self)

        self.ui.close_btn.clicked.connect(self.on_close)

    def on_close(self) -> None:
        self.close()
