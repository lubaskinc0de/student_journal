from PyQt6 import QtCore
from PyQt6.QtWidgets import QLabel, QMainWindow, QPushButton

from student_journal.presentation.widget.about import About


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.resize(500, 300)
        self.setMaximumSize(QtCore.QSize(500, 300))
        self.txt = QLabel(self)
        self.txt.setText("Дневник школьника")
        self.about_button = QPushButton(self)
        self.about_button.setText("O программе")

        self.about_button.clicked.connect(self.about)

    def about(self) -> None:
        self.about_form = About()
        self.about_form.show()
