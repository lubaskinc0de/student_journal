from dishka import Container
from PyQt6.QtWidgets import QListWidgetItem, QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.teacher.read_teacher import ReadTeacher
from student_journal.application.teacher.read_teachers import ReadTeachers
from student_journal.presentation.ui.teacher_list_ui import Ui_TeacherList
from student_journal.presentation.widget.teacher.edit_teacher import EditTeacher


class TeacherList(QWidget):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.container = container
        self.error_locator = container.get(ErrorLocator)
        self.current_form: None | EditTeacher = None

        self.ui = Ui_TeacherList()
        self.ui.setupUi(self)

        self.ui.refresh.clicked.connect(self.on_refresh)
        self.ui.add_more.clicked.connect(self.on_add_more)
        self.ui.list_teacher.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.load_teachers()

    def load_teachers(self) -> None:
        self.ui.list_teacher.clear()
        with self.container() as r_container:
            command = r_container.get(ReadTeachers)
            teachers = command.execute().teachers

        for teacher in teachers:
            item = QListWidgetItem(f"{teacher.full_name}")
            item.setData(0x100, teacher.teacher_id)
            self.ui.list_teacher.addItem(item)

    def on_refresh(self) -> None:
        self.load_teachers()

    def on_add_more(self) -> None:
        form = EditTeacher(self.container, teacher_id=None)
        self.current_form = form
        form.show()

    def on_item_double_clicked(self, item: QListWidgetItem) -> None:
        teacher_id = item.data(0x100)

        with self.container() as r_container:
            command = r_container.get(ReadTeacher)
            teacher = command.execute(teacher_id)

        form = EditTeacher(self.container, teacher_id=teacher.teacher_id)
        self.current_form = form
        form.show()
