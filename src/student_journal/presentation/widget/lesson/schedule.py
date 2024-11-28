from datetime import datetime

from dishka import Container
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QListWidgetItem, QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.lesson.read_first_lessons_of_weeks import (
    ReadFirstLessonsOfWeeks,
)
from student_journal.application.models.lesson import LessonsByDate
from student_journal.application.subject.read_subject import ReadSubject
from student_journal.domain.lesson import Lesson
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.presentation.ui.schedule_ui import Ui_Schedule
from student_journal.presentation.widget.lesson.edit_lesson import EditLesson
from student_journal.presentation.widget.month_year_picker import MonthYearPickerDialog


class Schedule(QWidget):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.container = container
        self.error_locator = container.get(ErrorLocator)
        self.current_form: None | EditLesson = None

        self.ui = Ui_Schedule()
        self.ui.setupUi(self)

        self.ui.refresh.clicked.connect(self.on_refresh)
        self.ui.month_year_picker.clicked.connect(self.open_month_year_picker)

        self.selected_month: int | None = None
        self.selected_year: int | None = None

        self.lessons_to_subjects: dict[LessonId, Subject] = {}
        self.all_lessons: list[Lesson] = []

        self.model = QStandardItemModel()
        self.ui.days_table.setModel(self.model)

        self.load_schedule()

    def load_schedule(self) -> None:
        self.ui.list_weeks.clear()
        self.model.clear()

        self.model.setHorizontalHeaderLabels(
            [
                "Понедельник",
                "Вторник",
                "Среда",
                "Четверг",
                "Пятница",
                "Суббота",
                "Воскресенье",
            ],
        )

        with self.container() as r_container:
            command = r_container.get(ReadFirstLessonsOfWeeks)
            lessons_by_date: LessonsByDate = command.execute()
            subject_command = r_container.get(ReadSubject)
            self.lessons_to_subjects.clear()

            for lesson in lessons_by_date.lessons.values():
                subject = subject_command.execute(lesson.subject_id)
                self.lessons_to_subjects[lesson.lesson_id] = subject

        weeks_with_lessons: dict[int, list[tuple[datetime, Lesson]]] = {}
        for date, lesson in lessons_by_date.lessons.items():
            week_number = date.isocalendar()[1]
            if week_number not in weeks_with_lessons:
                weeks_with_lessons[week_number] = []
            weeks_with_lessons[week_number].append((date, lesson))

        self.all_lessons.clear()

        for week_number, lessons in weeks_with_lessons.items():
            if lessons:
                widget_item = QListWidgetItem(f"Неделя {week_number}")
                widget_item.setData(0x100, week_number)
                self.ui.list_weeks.addItem(widget_item)

                week_schedule: dict[int, list[Lesson]] = {day: [] for day in range(7)}

                for date, lesson in lessons:
                    day_of_week = date.weekday()
                    week_schedule[day_of_week].append(lesson)

                for day in range(7):
                    if week_schedule[day]:
                        self.all_lessons.extend(week_schedule[day])

        for row_position in range(9):
            self.model.insertRow(row_position)
            for day in range(7):
                if row_position * 7 + day < len(self.all_lessons):
                    lesson = self.all_lessons[row_position * 7 + day]
                    subject_title = self.lessons_to_subjects[lesson.lesson_id].title
                    standart_item = QStandardItem(subject_title)
                else:
                    standart_item = QStandardItem("")

                standart_item.setFlags(
                    QtCore.Qt.ItemFlag.ItemIsSelectable
                    | QtCore.Qt.ItemFlag.ItemIsEnabled,
                )
                self.model.setItem(row_position, day, standart_item)

        for index in range(9 * 7, len(self.all_lessons)):
            row_position = self.model.rowCount()
            self.model.insertRow(row_position)
            for day in range(7):
                if index < len(self.all_lessons):
                    lesson = self.all_lessons[index]
                    subject_title = self.lessons_to_subjects[lesson.lesson_id].title
                    standart_item = QStandardItem(subject_title)
                else:
                    standart_item = QStandardItem("")

                standart_item.setFlags(
                    QtCore.Qt.ItemFlag.ItemIsSelectable
                    | QtCore.Qt.ItemFlag.ItemIsEnabled,
                )
                self.model.setItem(row_position, day, standart_item)

        self.ui.days_table.clicked.connect(self.on_lesson_clicked)

    def on_lesson_clicked(self, index: QtCore.QModelIndex) -> None:
        if index.isValid():
            item = self.model.item(index.row(), index.column())

            if item is not None and item.text():
                lesson_index = index.row() * 7 + index.column()
                if lesson_index < len(self.all_lessons):
                    lesson = self.all_lessons[lesson_index]

                    widget = EditLesson(self.container, lesson_id=lesson.lesson_id)
                    self.current = widget
                    self.current.show()

    def on_refresh(self) -> None:
        self.load_schedule()

    def open_month_year_picker(self) -> None:
        dialog = MonthYearPickerDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.selected_month = dialog.selected_month
            self.selected_year = dialog.selected_year
            self.load_schedule()
