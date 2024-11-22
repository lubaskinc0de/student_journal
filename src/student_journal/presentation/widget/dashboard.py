from dishka import Container
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QMenu, QStackedWidget, QWidget

from student_journal.presentation.widget.about import About
from student_journal.presentation.widget.edit_subject import EditSubject
from student_journal.presentation.widget.edit_teacher import EditTeacher


class Dashboard(QMainWindow):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.about_form = About()
        self.add_teacher_form = EditTeacher(container, None)
        self.add_subject_form = EditSubject(container, None)

        self.about_action = QAction("&О программе", self)
        self.add_teacher_action = QAction("&Добавить преподавателя", self)
        self.add_subject_action = QAction("&Добавить предмет", self)
        self.hometask_list_action = QAction("&Список заданий", self)
        self.subject_list_action = QAction("&Список предметов", self)
        self.teacher_list_action = QAction("&Список преподавателей", self)
        self.schedule_action = QAction("&Расписание", self)

        self.stacked_widget.addWidget(self.about_form)
        self.stacked_widget.addWidget(self.add_teacher_form)
        self.stacked_widget.addWidget(self.add_subject_form)

        self.add_teacher_action.triggered.connect(
            lambda: self.show_widget(self.add_teacher_form),
        )
        self.about_action.triggered.connect(
            lambda: self.show_widget(self.about_form),
        )
        self.add_subject_action.triggered.connect(
            lambda: self.show_widget(self.add_subject_form),
        )

        self.create_menu_bar()

    def show_widget(self, widget: QWidget) -> None:
        widget.show()
        self.stacked_widget.setCurrentWidget(widget)

    def create_menu_bar(self) -> None:
        menu_bar = self.menuBar()

        help_menu = QMenu("&Помощь", self)
        menu_bar.addMenu(help_menu)
        help_menu.addAction(self.about_action)

        teacher_menu = QMenu("&Преподаватели", self)
        menu_bar.addMenu(teacher_menu)
        teacher_menu.addAction(self.add_teacher_action)
        teacher_menu.addAction(self.teacher_list_action)

        subject_menu = QMenu("&Предметы", self)
        menu_bar.addMenu(subject_menu)
        subject_menu.addAction(self.add_subject_action)
        subject_menu.addAction(self.subject_list_action)

        hometask_menu = QMenu("&Задачи", self)
        menu_bar.addMenu(hometask_menu)
        hometask_menu.addAction(self.hometask_list_action)

        lesson_menu = QMenu("&Уроки", self)
        menu_bar.addMenu(lesson_menu)
        lesson_menu.addAction(self.schedule_action)

        student_menu = QMenu("&Профиль", self)
        menu_bar.addMenu(student_menu)
