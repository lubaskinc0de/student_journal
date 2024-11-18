from dishka import Container
from PyQt6.QtWidgets import QMainWindow, QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.exceptions.base import ApplicationError
from student_journal.application.student.create_student import CreateStudent, NewStudent
from student_journal.presentation.ui.register_ui import Ui_Register


class Register(QWidget):
    def __init__(
        self,
        container: Container,
        main: QMainWindow,
    ) -> None:
        super().__init__()

        self.container = container
        self.main = main
        self.error_locator = container.get(ErrorLocator)

        self.ui = Ui_Register()
        self.ui.setupUi(self)
        
        self.age = None
        self.avatar = None
        self.name = ""
        self.home_address = None
        self.timezone = None
        
        self.ui.submit_btn.clicked.connect(self.on_submit_btn)
        self.ui.name_input.textChanged.connect(self.on_name_input)
        self.ui.age_input.textChanged.connect(self.on_age_input)
        self.ui.address_input.textChanged.connect(self.on_address_input)
        self.ui.timezone_input.textChanged.connect(self.on_timezone_input)

    def on_submit_btn(self) -> None:
        try:
            with self.container() as r_container:
                data = NewStudent(
                    age=self.age,
                    name=self.name,
                    home_address=self.home_adress,
                    timezone=self.timezone,
                    avatar=None,
                )
                command = r_container.get(CreateStudent)
                command.execute(data)
        except ApplicationError as e:
            self.main.statusBar().showMessage(self.error_locator.get_text(e))

    def on_name_input(self) -> None:
        self.name = self.ui.name_input.text()

    def on_age_input(self) -> None:
        self.age = int(self.ui.age_input.text())

    def on_address_input(self) -> None:
        self.home_address = self.ui.address_input.text()

    def on_timezone_input(self) -> None:
        self.timezone = int(self.ui.timezone_input.text())
