from dishka import Container
from PyQt6 import QtGui
from PyQt6.QtWidgets import QListWidgetItem, QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.hometask.read_home_task import ReadHomeTask
from student_journal.application.hometask.read_home_tasks import ReadHomeTasks
from student_journal.application.lesson.read_lesson import ReadLesson
from student_journal.presentation.ui.hometask_list_ui import Ui_HometaskList
from student_journal.presentation.widget.hometask.edit_hometask import EditHomeTask


class HometaskList(QWidget):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.container = container
        self.error_locator = container.get(ErrorLocator)
        self.current_form: None | EditHomeTask = None

        self.ui = Ui_HometaskList()
        self.ui.setupUi(self)

        self.ui.refresh.clicked.connect(self.on_refresh)
        self.ui.show_done.stateChanged.connect(self.on_show_done_changed)
        self.ui.list_hometask.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.show_done = False
        self.load_home_tasks()

    def load_home_tasks(self) -> None:
        self.ui.list_hometask.clear()
        with self.container() as r_container:
            command = r_container.get(ReadHomeTasks)
            tasks = command.execute(self.show_done).home_tasks

        for task in tasks:
            item = QListWidgetItem(task.description)
            item.setData(0x100, task.task_id)

            if task.is_done:
                item.setForeground(QtGui.QColor("green"))

            self.ui.list_hometask.addItem(item)

    def on_refresh(self) -> None:
        self.load_home_tasks()

    def on_show_done_changed(self) -> None:
        self.show_done = self.ui.show_done.isChecked()
        self.load_home_tasks()

    def on_item_double_clicked(self, item: QListWidgetItem) -> None:
        task_id = item.data(0x100)

        with self.container() as r_container:
            command = r_container.get(ReadHomeTask)
            task = command.execute(task_id)

            read_lesson = r_container.get(ReadLesson)
            lesson = read_lesson.execute(task.lesson_id)

        form = EditHomeTask(self.container, task_id, lesson)
        self.current_form = form
        form.show()
