from dishka import Container
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.student.create_student import CreateStudent, NewStudent
from student_journal.presentation.ui.register_ui import Ui_Register


class Register(QWidget):
    finish = pyqtSignal(str)

    def __init__(
        self,
        container: Container,
    ) -> None:
        super().__init__()

        self.container = container
        self.error_locator = container.get(ErrorLocator)

        self.ui = Ui_Register()
        self.ui.setupUi(self)

        self.age: int | None = None
        self.avatar: str | None = None
        self.name: str = ""
        self.home_address: str | None = None
        self.timezone: int = 3

        self.ui.submit_btn.clicked.connect(self.on_submit_btn)
        self.ui.name_input.textChanged.connect(self.on_name_input)
        self.ui.age_input.valueChanged.connect(self.on_age_input)
        self.ui.address_input.textChanged.connect(self.on_address_input)
        self.ui.timezone_input.valueChanged.connect(self.on_timezone_input)
        self.ui.avatar_upload_btn.clicked.connect(self.on_avatar_upload_btn)

        self.update_avatar_preview()

    def update_avatar_preview(self) -> None:
        if self.avatar:
            pixmap = QPixmap(self.avatar)
            self.ui.avatar_preview.setPixmap(pixmap.scaled(100, 100))
        else:
            self.ui.avatar_preview.setText("Аватар не выбран")

    def on_submit_btn(self) -> None:
        with self.container() as r_container:
            data = NewStudent(
                age=self.age,
                name=self.name,
                home_address=self.home_address,
                timezone=self.timezone,
                avatar=self.avatar,
            )
            command = r_container.get(CreateStudent)
            student_id = command.execute(data)
        self.finish.emit(student_id.hex)

    def on_name_input(self) -> None:
        self.name = self.ui.name_input.text()

    def on_age_input(self) -> None:
        self.age = self.ui.age_input.value()

    def on_address_input(self) -> None:
        self.home_address = self.ui.address_input.text()

    def on_timezone_input(self) -> None:
        self.timezone = self.ui.timezone_input.value()

    def on_avatar_upload_btn(self) -> None:
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Выберите файл аватара",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp)",
        )
        if file_path:
            self.avatar = file_path
            self.update_avatar_preview()
