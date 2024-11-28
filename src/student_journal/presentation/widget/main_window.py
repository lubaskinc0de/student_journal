from uuid import UUID

from dishka import Container
from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from student_journal.adapters.id_provider import FileIdProvider
from student_journal.application.exceptions.student import (
    StudentIsNotAuthenticatedError,
)
from student_journal.domain.value_object.student_id import StudentId
from student_journal.presentation.widget.dashboard import Dashboard
from student_journal.presentation.widget.student.register import Register


class MainWindow(QMainWindow):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.container = container

        with self.container() as r_container:
            self.idp = r_container.get(FileIdProvider)
            self.dashboard: None | Dashboard = None

            self.register_form = Register(container)
            self.register_form.finish.connect(self.finish_register)

            self.stacked_widget = QStackedWidget()
            self.stacked_widget.addWidget(self.register_form)

            self.setCentralWidget(self.stacked_widget)

            try:
                self.idp.ensure_authenticated()
            except StudentIsNotAuthenticatedError:
                self.display_register()
                return
            else:
                self.display_dashboard()

    def display_register(self) -> None:
        self.stacked_widget.setCurrentWidget(self.register_form)

    def display_dashboard(self) -> None:
        self.dashboard = Dashboard(self.container)
        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.setCurrentWidget(self.dashboard)

    def finish_register(self, student_id: str) -> None:
        student_id_uuid = StudentId(UUID(student_id))
        self.idp.save(student_id_uuid)
        self.display_dashboard()
