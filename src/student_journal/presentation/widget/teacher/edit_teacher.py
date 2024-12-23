from dishka import Container
from PyQt6.QtWidgets import QWidget

from student_journal.adapters.exceptions.ui.teacher import (
    FullNameNotSpecifiedError,
    TeacherIsNotSpecifiedError,
)
from student_journal.application.teacher import (
    CreateTeacher,
    DeleteTeacher,
    NewTeacher,
    ReadTeacher,
    UpdatedTeacher,
    UpdateTeacher,
)
from student_journal.domain.value_object.teacher_id import TeacherId
from student_journal.presentation.ui.edit_teacher_ui import Ui_EditTeacher


class EditTeacher(QWidget):
    def __init__(
        self,
        container: Container,
        teacher_id: TeacherId | None,
    ) -> None:
        super().__init__()

        self.container = container
        self.teacher_id = teacher_id

        self.ui = Ui_EditTeacher()
        self.ui.setupUi(self)

        self.full_name: str | None = None

        self.ui.submit_btn.clicked.connect(self.on_submit_btn)
        self.ui.delete_btn.clicked.connect(self.on_delete_btn)
        self.ui.full_name_input.textChanged.connect(self.on_full_name_input)

        if not self.teacher_id:
            self.ui.delete_btn.hide()
            self.ui.main_label.setText("Добавить учителя")
        else:
            with self.container() as r_container:
                command = r_container.get(ReadTeacher)
                teacher = command.execute(self.teacher_id)
                self.ui.full_name_input.setText(teacher.full_name)
                self.full_name = teacher.full_name

            self.ui.main_label.setText("Редактировать учителя")

    def on_submit_btn(self) -> None:
        if not self.full_name:
            raise FullNameNotSpecifiedError

        with self.container() as r_container:
            if not self.teacher_id:
                data = NewTeacher(
                    full_name=self.full_name,
                    avatar=None,
                )
                command = r_container.get(CreateTeacher)
                command.execute(data)
            else:
                data_update = UpdatedTeacher(
                    teacher_id=self.teacher_id,
                    full_name=self.full_name,
                    avatar=None,
                )
                command_update = r_container.get(UpdateTeacher)
                command_update.execute(data_update)
        self.close()

    def on_delete_btn(self) -> None:
        if not self.teacher_id:
            raise TeacherIsNotSpecifiedError

        with self.container() as r_container:
            command = r_container.get(DeleteTeacher)
            command.execute(self.teacher_id)
        self.close()

    def on_full_name_input(self) -> None:
        self.full_name = self.ui.full_name_input.text()
