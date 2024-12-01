from datetime import date, timedelta

from dishka import Container
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox, QPushButton, QWidget

from student_journal.adapters.exceptions.ui.schedule import (
    WeekPeriodUnsetError,
    WeekStartUnsetError,
)
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.lesson.delete_all_lessons import DeleteAllLessons
from student_journal.application.lesson.delete_lessons_for_week import (
    DeleteLessonsForWeek,
)
from student_journal.application.lesson.read_first_lessons_of_weeks import (
    ReadFirstLessonsOfWeeks,
)
from student_journal.application.lesson.read_lessons_for_week import ReadLessonsForWeek
from student_journal.application.models.lesson import LessonsByDate
from student_journal.domain.lesson import Lesson
from student_journal.domain.subject import Subject
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.presentation.ui.schedule_ui import Ui_Schedule
from student_journal.presentation.widget.lesson.edit_lesson import EditLesson
from student_journal.presentation.widget.month_year_picker import MonthYearPickerDialog

WEEK_DAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
]


class Schedule(QWidget):
    def __init__(self, container: Container) -> None:
        super().__init__()

        self.container = container
        self.ui = Ui_Schedule()
        self.ui.setupUi(self)

        self.ui.refresh.clicked.connect(self.on_refresh)
        self.ui.month_year_picker.clicked.connect(self.open_month_year_picker)
        self.ui.list_weeks.itemClicked.connect(self.on_week_clicked)
        self.ui.clear_week_lessons.clicked.connect(self.clear_week_lessons_handler)
        self.ui.clear_all_lessons.clicked.connect(self.clear_all_lessons_handler)
        self.ui.days_table.doubleClicked.connect(self.on_lesson_clicked)

        self.selected_month: int | None = None
        self.selected_year: int | None = None
        self.current_widget: QWidget | None = None
        self.week_start: None | date = None

        self.model = QStandardItemModel()
        self.ui.days_table.setModel(self.model)
        self.ui.days_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch,
        )

        self.load_schedule()
        self.place_add_buttons()

    def place_add_buttons(self) -> None:
        buttons = [QPushButton(week_day) for week_day in WEEK_DAYS]

        layout = self.ui.button_container

        for btn in buttons:
            layout.addWidget(btn)
            btn.clicked.connect(self.add_new_lesson)

    def add_new_lesson(self) -> None:
        if not self.week_start:
            raise WeekStartUnsetError

        if not isinstance(sender := self.sender(), QPushButton):
            return

        week_day_name = sender.text()
        week_day = WEEK_DAYS.index(week_day_name)
        at = self.week_start + timedelta(days=week_day)
        form = EditLesson(self.container, lesson_id=None, lesson_at=(at, None))
        self.current_widget = form

        self.current_widget.show()

    def clear_week_lessons_handler(self) -> None:
        if not self.week_start:
            raise WeekStartUnsetError

        reply = QMessageBox.question(
            self,
            "Очистить расписание?",
            "Вы уверены, что хотите продолжить? "
            f"Это сотрет все уроки в текущей неделе "
            f"(старт {self.week_start.strftime('%d.%m.%Y')})",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.No:
            return

        with self.container() as r_container:
            command = r_container.get(DeleteLessonsForWeek)
            command.execute(self.week_start)

        self.load_weeks()
        self.load_schedule()

        QMessageBox.information(
            self,
            "Операция завершена",
            "Удаление уроков текущей недели прошло успешно",
            QMessageBox.StandardButton.Ok,
        )

    def clear_all_lessons_handler(self) -> None:
        reply = QMessageBox.question(
            self,
            "Очистить ВСЕ уроки?",
            "Это СОТРЕТ ВСЕ уроки ЗА ВСЕ недели. Это действие нельзя будет отменить.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.No:
            return

        with self.container() as r_container:
            command = r_container.get(DeleteAllLessons)
            command.execute()

        self.load_weeks()
        self.load_schedule()

        QMessageBox.information(
            self,
            "Операция завершена",
            "Все уроки удалены",
            QMessageBox.StandardButton.Ok,
        )

    def fetch_weeks(self, month: int, year: int) -> LessonsByDate:
        with self.container() as r_container:
            command = r_container.get(ReadFirstLessonsOfWeeks)
            lessons_by_date: LessonsByDate = command.execute(month, year)
        return lessons_by_date

    def load_weeks(self) -> None:
        if not self.selected_month or not self.selected_year:
            raise WeekPeriodUnsetError

        self.ui.list_weeks.clear()
        lessons_by_date = self.fetch_weeks(self.selected_month, self.selected_year)
        self.populate_week_list(lessons_by_date)

    def load_lessons_for_week(self, week_start: date) -> dict[date, list[Lesson]]:
        with self.container() as r_container:
            command = r_container.get(ReadLessonsForWeek)
            lessons = command.execute(week_start).lessons
        return lessons

    def fetch_subjects_for_lessons(
        self,
        lessons: list[LessonId],
    ) -> dict[LessonId, Subject]:
        with self.container() as r_container:
            gateway = r_container.get(LessonGateway)
            return gateway.read_subjects_for_lessons(lessons)  # type: ignore

    def load_schedule(self) -> None:
        self.clear_schedule()

        if not self.week_start:
            return

        headers = []
        for i, week_day in enumerate(WEEK_DAYS):
            current_date = self.week_start + timedelta(days=i)
            date_str = current_date.strftime("%d.%m")
            headers.append(f"{week_day} ({date_str})")

        self.model.setHorizontalHeaderLabels(headers)

        lessons = self.load_lessons_for_week(self.week_start)
        ids = []

        for each in lessons.values():
            ids.extend([lesson.lesson_id for lesson in each])

        subject_for_lessons = self.fetch_subjects_for_lessons(ids)
        self.populate_schedule(lessons, subject_for_lessons)

    def clear_schedule(self) -> None:
        self.model.clear()
        self.model.setHorizontalHeaderLabels(WEEK_DAYS)

    def populate_week_list(self, lessons_by_date: LessonsByDate) -> None:
        weeks_with_lessons = {}
        for da_te in lessons_by_date.lessons:
            week_start = da_te - timedelta(days=da_te.weekday())
            week_end = week_start + timedelta(days=6)

            start_formatted = week_start.strftime("%d.%m")
            end_formatted = week_end.strftime("%d.%m")
            week = f"с {start_formatted} по {end_formatted}"

            weeks_with_lessons[week] = week_start

        for week, start in weeks_with_lessons.items():
            widget_item = QListWidgetItem(f"{week}")
            widget_item.setData(0x100, start)
            self.ui.list_weeks.addItem(widget_item)

    def populate_schedule(
        self,
        lessons: dict[date, list[Lesson]],
        lessons_subjects: dict[LessonId, Subject],
    ) -> None:
        for da_te, lessons_in_date in lessons.items():
            week_days_count = len(WEEK_DAYS) - 1
            column = da_te.weekday()

            if column > week_days_count:
                continue
            for row, lesson in enumerate(lessons_in_date):
                subject_title = lessons_subjects[lesson.lesson_id].title
                formatted_time = lesson.at.time().strftime("%H:%M")

                item_title = f"{subject_title} ({formatted_time})"
                item = QStandardItem(item_title)
                item.setFlags(
                    QtCore.Qt.ItemFlag.ItemIsSelectable
                    | QtCore.Qt.ItemFlag.ItemIsEnabled,
                )
                item.setData(lesson.lesson_id, role=0x100)
                self.model.setItem(row, column, item)

    def on_lesson_clicked(self, index: QtCore.QModelIndex) -> None:
        if index.isValid():
            item = self.model.item(index.row(), index.column())
            lesson_id = item.data(0x100)

            widget = EditLesson(self.container, lesson_id=lesson_id)
            self.current_widget = widget
            self.current_widget.show()

    def on_week_clicked(self, item: QListWidgetItem) -> None:
        self.week_start = item.data(0x100)
        self.load_schedule()

    def on_refresh(self) -> None:
        self.load_weeks()
        self.load_schedule()

    def open_month_year_picker(self) -> None:
        dialog = MonthYearPickerDialog(self)

        if self.selected_month and self.selected_year:
            dialog.set_initial_selection(self.selected_month, self.selected_year)

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.selected_month = dialog.selected_month
            self.selected_year = dialog.selected_year
            self.load_weeks()
