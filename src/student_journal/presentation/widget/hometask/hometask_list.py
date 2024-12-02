from dishka import Container
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QListWidgetItem, QWidget

from student_journal.application.hometask.delete_home_task import DeleteHomeTask
from student_journal.application.hometask.read_home_task import ReadHomeTask
from student_journal.application.hometask.read_home_tasks import ReadHomeTasks
from student_journal.application.hometask.update_home_task import (
    UpdatedHomeTask,
    UpdateHomeTask,
)
from student_journal.application.lesson.read_lesson import ReadLesson
from student_journal.application.subject.read_subject import ReadSubject
from student_journal.domain.value_object.task_id import HomeTaskId
from student_journal.presentation.ui.hometask_list_ui import Ui_HometaskList
from student_journal.presentation.widget.hometask.edit_hometask import EditHomeTask


class HomeTaskList(QWidget):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.container = container
        self.current_widget: None | EditHomeTask = None

        self.ui = Ui_HometaskList()
        self.ui.setupUi(self)

        self.ui.refresh.clicked.connect(self.on_refresh)
        self.ui.show_done.stateChanged.connect(self.on_show_done_changed)
        self.ui.list_hometask.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.ui.list_hometask.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu,
        )
        self.ui.list_hometask.customContextMenuRequested.connect(self.on_context_menu)

        self.show_done = False
        self.load_home_tasks()

    def load_home_tasks(self) -> None:
        self.ui.list_hometask.clear()
        with self.container() as r_container:
            command = r_container.get(ReadHomeTasks)
            read_subject = r_container.get(ReadSubject)
            read_lesson = r_container.get(ReadLesson)
            tasks = command.execute(self.show_done).home_tasks

            for task in tasks:
                lesson = read_lesson.execute(task.lesson_id)
                subject = read_subject.execute(lesson.subject_id)

                task_text = f"{subject.title}: {task.description[:50]}"

                item = QListWidgetItem(task_text)
                item.setData(0x100, task.task_id)

                font = item.font()
                font.setPointSize(font.pointSize() + 4)
                item.setFont(font)

                if task.is_done:
                    item.setForeground(QtGui.QColor("green"))
                else:
                    item.setForeground(QtGui.QColor("red"))

                self.ui.list_hometask.addItem(item)

    def on_refresh(self) -> None:
        self.load_home_tasks()

    def on_show_done_changed(self) -> None:
        self.show_done = self.ui.show_done.isChecked()
        self.load_home_tasks()

    def on_item_double_clicked(self, item: QListWidgetItem) -> None:
        task_id: HomeTaskId = item.data(0x100)

        with self.container() as r_container:
            command = r_container.get(ReadHomeTask)
            task = command.execute(task_id)

            read_lesson = r_container.get(ReadLesson)
            lesson = read_lesson.execute(task.lesson_id)

        form = EditHomeTask(self.container, task_id, lesson)
        self.current_widget = form
        form.show()

    def on_context_menu(self, position: QtCore.QPoint) -> None:
        item = self.ui.list_hometask.itemAt(position)
        if item is not None:
            menu = QtWidgets.QMenu()
            mark_done_action = menu.addAction("Выполнено")
            delete_action = menu.addAction("Удалить")

            mark_done_action.triggered.connect(lambda: self.mark_task_done(item))
            delete_action.triggered.connect(lambda: self.delete_task(item))

            menu.exec(self.ui.list_hometask.viewport().mapToGlobal(position))

    def mark_task_done(self, item: QListWidgetItem) -> None:
        task_id: HomeTaskId = item.data(0x100)
        with self.container() as r_container:
            read_task = r_container.get(ReadHomeTask)
            task = read_task.execute(task_id)
            update_command = r_container.get(UpdateHomeTask)
            updated_task = UpdatedHomeTask(
                task_id=task.task_id,
                lesson_id=task.lesson_id,
                description=task.description,
                is_done=True,
            )
            update_command.execute(updated_task)
        self.load_home_tasks()

    def delete_task(self, item: QListWidgetItem) -> None:
        task_id: HomeTaskId = item.data(0x100)
        with self.container() as r_container:
            delete_command = r_container.get(DeleteHomeTask)
            delete_command.execute(task_id)
        self.load_home_tasks()
