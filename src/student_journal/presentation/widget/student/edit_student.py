from dishka import Container
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.student.read_current_student import ReadCurrentStudent
from student_journal.application.student.update_student import (
    UpdatedStudent,
    UpdateStudent,
)
from student_journal.presentation.ui.edit_student import EditStudentUI


class EditStudent(QWidget):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.container = container
        self.error_locator = container.get(ErrorLocator)

        self.ui = EditStudentUI()
        self.ui.setupUi(self)

        self.name = ""
        self.age: int | None = None
        self.home_address: str | None = None
        self.avatar: str | None = None

        self.ui.submit_btn.clicked.connect(self.on_submit_btn)
        self.ui.cancel_btn.clicked.connect(self.on_cancel_btn)
        self.ui.name_input.textChanged.connect(self.on_name_input)
        self.ui.age_input.valueChanged.connect(self.on_age_input)
        self.ui.address_input.textChanged.connect(self.on_address_input)
        self.ui.avatar_upload_btn.clicked.connect(self.on_avatar_upload_btn)
        self.ui.refresh.clicked.connect(self.refresh_avg_mark)

        self.load_student()

    def load_student(self) -> None:
        with self.container() as r_container:
            command = r_container.get(ReadCurrentStudent)
            student = command.execute()

            self.ui.name_input.setText(student.name)
            self.name = student.name

            if student.age:
                self.age = student.age
                self.ui.age_input.setValue(student.age)
            if student.home_address:
                self.home_address = student.home_address
                self.ui.address_input.setText(student.home_address)

            self.ui.avg_mark.setValue(student.student_overall_avg_mark)

            self.avatar = student.avatar
            self.update_avatar_preview()

    def refresh_avg_mark(self) -> None:
        with self.container() as r_container:
            command = r_container.get(ReadCurrentStudent)
            student = command.execute()
            self.ui.avg_mark.setValue(student.student_overall_avg_mark)

    def update_avatar_preview(self) -> None:
        if self.avatar:
            pixmap = QPixmap(self.avatar)
            self.ui.avatar_preview.setPixmap(
                pixmap.scaled(100, 100),
            )
        else:
            self.ui.avatar_preview.setText("Аватар не выбран")

    def on_submit_btn(self) -> None:
        with self.container() as r_container:
            data = UpdatedStudent(
                name=self.name,
                age=self.age,
                home_address=self.home_address,
                avatar=self.avatar,
            )
            command = r_container.get(UpdateStudent)
            command.execute(data)
        self.close()

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

    def on_cancel_btn(self) -> None:
        self.load_student()
