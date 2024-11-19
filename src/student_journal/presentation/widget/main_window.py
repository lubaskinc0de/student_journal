from uuid import UUID

from dishka import Container
from PyQt6.QtWidgets import QMainWindow

from student_journal.adapters.id_provider import FileIdProvider
from student_journal.application.exceptions.student import (
    StudentIsNotAuthenticatedError,
)
from student_journal.domain.value_object.student_id import StudentId
from student_journal.presentation.widget.dashboard import Dashboard
from student_journal.presentation.widget.register import Register


class MainWindow(QMainWindow):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.container = container
        self.idp = container.get(FileIdProvider)
        self.register_form = Register(container, self)
        self.dashboard = Dashboard(container)

        try:
            self.idp.ensure_is_auth()
        except StudentIsNotAuthenticatedError:
            self.register()
            return
        else:
            self.setCentralWidget(self.dashboard)
            self.dashboard.show()

    def register(self) -> None:
        self.setCentralWidget(self.register_form)
        self.register_form.finish.connect(self.finish_register)
        self.register_form.show()

    def finish_register(self, student_id: str) -> None:
        student_id_uuid = StudentId(UUID(student_id))
        self.idp.save(student_id_uuid)
        self.setCentralWidget(self.dashboard)
        self.dashboard.show()
