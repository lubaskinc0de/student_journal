from dishka import Container
from PyQt6.QtWidgets import QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.hometask.create_home_task import (
    CreateHomeTask,
    NewHomeTask,
)
from student_journal.application.hometask.delete_home_task import DeleteHomeTask
from student_journal.application.hometask.update_home_task import (
    UpdatedHomeTask,
    UpdateHomeTask,
)
from student_journal.application.subject.read_subject import ReadSubject
from student_journal.domain.lesson import Lesson
from student_journal.domain.value_object.task_id import HomeTaskId
from student_journal.presentation.ui.edit_hometask_ui import Ui_EditHometask


class EditHomeTask(QWidget):
    def __init__(
        self,
        container: Container,
        home_task_id: HomeTaskId | None,
        lesson: Lesson,
    ) -> None:
        super().__init__()

        self.container = container
        self.home_task_id = home_task_id
        self.lesson = lesson
        self.error_locator = container.get(ErrorLocator)

        self.ui = Ui_EditHometask()
        self.ui.setupUi(self)

        self.is_done: bool = False
        self.description: str = ""

        self.ui.submit_btn.clicked.connect(self.on_submit_btn)
        self.ui.delete_btn.clicked.connect(self.on_delete_btn)
        self.ui.is_done.stateChanged.connect(self.on_is_done_changed)
        self.ui.description.textChanged.connect(self.on_description_changed)

        if not self.home_task_id:
            self.ui.delete_btn.hide()
            self.ui.main_label.setText("Добавить ДЗ")
        else:
            self.ui.main_label.setText("Редактирование ДЗ")

        self.load_lessons()

    def load_lessons(self) -> None:
        self.ui.lesson.clear()
        with self.container() as r_container:
            subject = r_container.get(ReadSubject).execute(
                self.lesson.subject_id,
            )

        self.ui.lesson.addItem(subject.title, self.lesson.lesson_id)
        self.ui.lesson.setEnabled(False)

    def on_submit_btn(self) -> None:
        lesson_id = self.lesson.lesson_id

        with self.container() as r_container:
            if not self.home_task_id:
                data = NewHomeTask(
                    lesson_id=lesson_id,
                    description=self.description,
                    is_done=self.is_done,
                )
                command = r_container.get(CreateHomeTask)
                command.execute(data)
            else:
                data_update = UpdatedHomeTask(
                    task_id=self.home_task_id,
                    lesson_id=lesson_id,
                    description=self.description,
                    is_done=self.is_done,
                )
                command_update = r_container.get(UpdateHomeTask)
                command_update.execute(data_update)
        self.close()

    def on_delete_btn(self) -> None:
        if not self.home_task_id:
            return

        with self.container() as r_container:
            command = r_container.get(DeleteHomeTask)
            command.execute(self.home_task_id)

        self.close()

    def on_is_done_changed(self) -> None:
        self.is_done = self.ui.is_done.isChecked()

    def on_description_changed(self) -> None:
        self.description = self.ui.description.toPlainText()
