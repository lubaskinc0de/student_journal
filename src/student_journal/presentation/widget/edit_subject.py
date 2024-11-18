from uuid import UUID

from dishka import Container
from PyQt6.QtWidgets import QMainWindow, QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.exceptions.base import ApplicationError
from student_journal.application.subject.create_subject import CreateSubject, NewSubject
from student_journal.application.subject.delete_subject import DeleteSubject
from student_journal.application.subject.update_subject import (
    UpdatedSubject,
    UpdateSubject,
)
from student_journal.application.teacher import ReadTeachers
from student_journal.domain.value_object.subject_id import SubjectId
from student_journal.domain.value_object.teacher_id import TeacherId
from student_journal.presentation.ui.edit_subject_ui import Ui_EditSubject


class EditSubject(QWidget):
    def __init__(
        self,
        container: Container,
        main_window: QMainWindow,
        subject_id: SubjectId | None,
    ) -> None:
        super().__init__()

        self.container = container
        self.main = main_window
        self.subject_id = subject_id
        self.error_locator = container.get(ErrorLocator)

        self.ui = Ui_EditSubject()
        self.ui.setupUi(self)

        self.title = ""
        self.teacher_id: str | None = None

        self.ui.submit_btn.clicked.connect(self.on_submit_btn)
        self.ui.delete_btn.clicked.connect(self.on_delete_btn)
        self.ui.title_input.textChanged.connect(self.on_title_input)
        self.ui.teacher_combo.currentIndexChanged.connect(self.on_teacher_combo_changed)

        if not self.subject_id:
            self.ui.delete_btn.hide()
            self.ui.main_label.setText("Добавить предмет")
        else:
            self.ui.main_label.setText("Редактировать предмет")

        self.load_teachers()

    def load_teachers(self) -> None:
        try:
            with self.container() as r_container:
                teachers = r_container.get(ReadTeachers).execute().teachers
                self.ui.teacher_combo.clear()
                for teacher in teachers:
                    self.ui.teacher_combo.addItem(teacher.full_name, teacher.teacher_id)
        except ApplicationError as e:
            self.main.statusBar().showMessage(self.error_locator.get_text(e))

    def on_submit_btn(self) -> None:
        if not self.teacher_id:
            return

        teacher_id = TeacherId(UUID(self.teacher_id))
        try:
            with self.container() as r_container:
                if not self.subject_id:
                    data = NewSubject(
                        title=self.title,
                        teacher_id=teacher_id,
                    )
                    command = r_container.get(CreateSubject)
                    command.execute(data)
                else:
                    data_update = UpdatedSubject(
                        subject_id=self.subject_id,
                        title=self.title,
                        teacher_id=teacher_id,
                    )
                    command_update = r_container.get(UpdateSubject)
                    command_update.execute(data_update)
        except ApplicationError as e:
            self.main.statusBar().showMessage(self.error_locator.get_text(e))
        else:
            self.close()

    def on_delete_btn(self) -> None:
        if not self.subject_id:
            return

        try:
            with self.container() as r_container:
                command = r_container.get(DeleteSubject)
                command.execute(self.subject_id)
        except ApplicationError as e:
            self.main.statusBar().showMessage(self.error_locator.get_text(e))
        else:
            self.close()

    def on_title_input(self) -> None:
        self.title = self.ui.title_input.text()

    def on_teacher_combo_changed(self) -> None:
        self.teacher_id = self.ui.teacher_combo.currentData()
