from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MonthYearPickerDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Выбор месяца и года")
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
            }
            QComboBox {
                font-size: 14px;
                padding: 5px;
                margin: 5px 0;
            }
            QPushButton {
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #39843c;
            }
        """)

        layout = QVBoxLayout(self)
        self.label = QLabel("Выберите месяц и год:", self)
        layout.addWidget(self.label)

        self.month_combo = QComboBox(self)
        self.month_combo.addItems(
            [
                "Январь",
                "Февраль",
                "Март",
                "Апрель",
                "Май",
                "Июнь",
                "Июль",
                "Август",
                "Сентябрь",
                "Октябрь",
                "Ноябрь",
                "Декабрь",
            ],
        )
        layout.addWidget(self.month_combo)

        self.year_combo = QComboBox(self)
        current_year = QDate.currentDate().year()
        self.year_combo.addItems(
            [str(year) for year in tuple(range(current_year - 50, current_year + 51))],
        )
        self.year_combo.setCurrentText(str(current_year))
        layout.addWidget(self.year_combo)

        self.confirm_button = QPushButton("Выбрать", self)
        self.confirm_button.clicked.connect(self.accept_selection)
        layout.addWidget(self.confirm_button)

        self.selected_month: int | None = None
        self.selected_year: int | None = None

    def accept_selection(self) -> None:
        self.selected_month = self.month_combo.currentIndex() + 1
        self.selected_year = int(self.year_combo.currentText())
        self.accept()
