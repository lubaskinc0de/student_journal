from dishka import Container
from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QMenu

from student_journal.presentation.widget.about import About
from student_journal.presentation.widget.edit_teacher import EditTeacher


class Dashboard(QMainWindow):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.about_form = About()
        self.add_teacher_form = EditTeacher(container, self, None)

        self.about_action = QAction("&О программе", self)
        self.about_action.triggered.connect(self.about_form.show)

        self.add_teacher_action = QAction("&Добавить преподавателя", self)
        self.add_teacher_action.triggered.connect(self.add_teacher_form.show)

        self.init_ui()
        self.create_menu_bar()

    def init_ui(self) -> None:
        self.resize(500, 300)
        self.setMaximumSize(QtCore.QSize(500, 300))

    def create_menu_bar(self) -> None:
        menu_bar = self.menuBar()

        help_menu = QMenu("&Помощь", self)
        menu_bar.addMenu(help_menu)
        help_menu.addAction(self.about_action)

        teacher_menu = QMenu("&Преподаватели", self)
        menu_bar.addMenu(teacher_menu)
        teacher_menu.addAction(self.add_teacher_action)

        subject_menu = QMenu("&Предметы", self)
        menu_bar.addMenu(subject_menu)

        hometask_menu = QMenu("&Задачи", self)
        menu_bar.addMenu(hometask_menu)

        lesson_menu = QMenu("&Уроки", self)
        menu_bar.addMenu(lesson_menu)

        student_menu = QMenu("&Профиль", self)
        menu_bar.addMenu(student_menu)
