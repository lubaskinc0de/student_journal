from dishka import Container
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QWidget

from student_journal.adapters.exceptions.ui.student import NameNotSpecifiedError
from student_journal.adapters.id_provider import FileIdProvider
from student_journal.adapters.load_test_data import TestDataLoader
from student_journal.application.common.id_provider import IdProvider
from student_journal.application.student.create_student import CreateStudent, NewStudent
from student_journal.presentation.ui.register import RegisterUI


class Register(QWidget):
    finish = pyqtSignal(str)

    def __init__(
        self,
        container: Container,
    ) -> None:
        super().__init__()

        self.container = container
        self.ui = RegisterUI()
        self.ui.setupUi(self)

        self.age: int | None = None
        self.avatar: str | None = None
        self.name: str | None = None
        self.home_address: str | None = None

        self.ui.submit_btn.clicked.connect(self.on_submit_btn)
        self.ui.name_input.textChanged.connect(self.on_name_input)
        self.ui.age_input.valueChanged.connect(self.on_age_input)
        self.ui.address_input.textChanged.connect(self.on_address_input)
        self.ui.avatar_upload_btn.clicked.connect(self.on_avatar_upload_btn)
        self.ui.insert_test_data.clicked.connect(self.on_insert_test_data)

        self.update_avatar_preview()

    def update_avatar_preview(self) -> None:
        if self.avatar:
            pixmap = QPixmap(self.avatar)
            self.ui.avatar_preview.setPixmap(pixmap.scaled(100, 100))
        else:
            self.ui.avatar_preview.setText("Аватар не выбран")

    def on_submit_btn(self) -> None:
        if not self.name:
            raise NameNotSpecifiedError

        with self.container() as r_container:
            idp = r_container.get(FileIdProvider)
            data = NewStudent(
                age=self.age,
                name=self.name,
                home_address=self.home_address,
                avatar=self.avatar,
            )
            command = r_container.get(CreateStudent)
            student_id = command.execute(data)
            idp.save(student_id)
        self.finish.emit(student_id.hex)

    def on_insert_test_data(self) -> None:
        reply = QMessageBox.question(
            self,
            "Вы уверены?",
            "Эта операция заполнит приложение тестовыми данными "
            "(операция может занять какое-то время). "
            "Атомарность операции не гарантируется",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.No:
            return

        with self.container() as r_container:
            loader = r_container.get(TestDataLoader)
            idp = r_container.get(FileIdProvider)
            student_id = loader.insert_student()
            idp.save(student_id)

        with self.container() as r_container:
            loader = r_container.get(TestDataLoader)
            idp = r_container.get(IdProvider)
            loader.insert_data(idp.get_id())

        QMessageBox.information(
            self,
            "Операция завершена",
            "Данные загружены",
            QMessageBox.StandardButton.Ok,
        )

        self.finish.emit(student_id.hex)

    def on_name_input(self) -> None:
        self.name = self.ui.name_input.text()

    def on_age_input(self) -> None:
        self.age = self.ui.age_input.value()

    def on_address_input(self) -> None:
        self.home_address = self.ui.address_input.text()

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
