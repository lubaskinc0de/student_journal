from dishka import Container
from PyQt6.QtWidgets import QListWidgetItem, QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.subject.read_subject import ReadSubject
from student_journal.application.subject.read_subjects import ReadSubjects
from student_journal.presentation.ui.subject_list_ui import Ui_SubjectList
from student_journal.presentation.widget.subject.edit_subject import EditSubject


class SubjectList(QWidget):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.container = container
        self.error_locator = container.get(ErrorLocator)
        self.current_form: None | EditSubject = None

        self.ui = Ui_SubjectList()
        self.ui.setupUi(self)

        self.ui.refresh.clicked.connect(self.on_refresh)
        self.ui.add_more.clicked.connect(self.on_add_more)
        self.ui.list_subject.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.load_subjects()

    def load_subjects(self) -> None:
        self.ui.list_subject.clear()
        with self.container() as r_container:
            command = r_container.get(ReadSubjects)
            subjects = command.execute()

        for subject in subjects:
            item = QListWidgetItem(subject.title)
            item.setData(0x100, subject.subject_id)
            self.ui.list_subject.addItem(item)

    def on_refresh(self) -> None:
        self.load_subjects()

    def on_add_more(self) -> None:
        form = EditSubject(self.container, subject_id=None)
        self.current_form = form
        form.show()

    def on_item_double_clicked(self, item: QListWidgetItem) -> None:
        subject_id = item.data(0x100)

        with self.container() as r_container:
            command = r_container.get(ReadSubject)
            subject = command.execute(subject_id)

        form = EditSubject(self.container, subject_id=subject.subject_id)
        self.current_form = form
        form.show()
