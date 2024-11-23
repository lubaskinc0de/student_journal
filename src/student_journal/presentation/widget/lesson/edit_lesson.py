from datetime import date, datetime, time

from dishka import Container
from PyQt6.QtWidgets import QCalendarWidget, QDialog, QPushButton, QVBoxLayout, QWidget

from student_journal.adapters.error_locator import ErrorLocator
from student_journal.application.lesson.create_lesson import CreateLesson, NewLesson
from student_journal.application.lesson.delete_lesson import DeleteLesson
from student_journal.application.lesson.read_lesson import ReadLesson
from student_journal.application.lesson.update_lesson import (
    UpdatedLesson,
    UpdateLesson,
)
from student_journal.application.subject.read_subjects import ReadSubjects
from student_journal.domain.value_object.lesson_id import LessonId
from student_journal.domain.value_object.subject_id import SubjectId
from student_journal.presentation.ui.edit_lesson_ui import Ui_EditLesson


class EditLesson(QWidget):
    def __init__(self, container: Container, lesson_id: LessonId | None) -> None:
        super().__init__()

        self.container = container
        self.lesson_id = lesson_id
        self.error_locator = container.get(ErrorLocator)

        self.ui = Ui_EditLesson()
        self.ui.setupUi(self)

        self.subject_id: SubjectId | None = None
        self.lesson_date: None | date = None
        self.lesson_time: None | time = None
        self.date_time: None | datetime = None
        self.note = ""
        self.mark = 0
        self.room = 0
        self.index_number = 0

        self.ui.submit_btn.clicked.connect(self.on_submit_btn)
        self.ui.delete_btn.clicked.connect(self.on_delete_btn)
        self.ui.subject_combo.currentIndexChanged.connect(self.on_subject_combo_changed)
        self.ui.time_edit.timeChanged.connect(self.on_time_changed)
        self.ui.note_edit.textChanged.connect(self.on_note_edit_changed)
        self.ui.mark_spinbox.valueChanged.connect(self.on_mark_changed)
        self.ui.room_spinbox.valueChanged.connect(self.on_room_changed)
        self.ui.index_number_spinbox.valueChanged.connect(self.on_index_number_changed)
        self.ui.refresh.clicked.connect(self.load_subjects)
        self.ui.date_popup.clicked.connect(self.open_calendar_dialog)

        self.load_subjects()

        if not self.lesson_id:
            self.ui.delete_btn.hide()
            self.ui.main_label.setText("Добавить урок")
        else:
            self.ui.main_label.setText("Редактировать урок")
            self.load_lesson()

    def load_subjects(self) -> None:
        with self.container() as r_container:
            subjects = r_container.get(ReadSubjects).execute()
            self.ui.subject_combo.clear()
            for subject in subjects:
                self.ui.subject_combo.addItem(subject.title, subject.subject_id)

    def load_lesson(self) -> None:
        if not self.lesson_id:
            return

        with self.container() as r_container:
            command = r_container.get(ReadLesson)
            lesson = command.execute(self.lesson_id)

            self.ui.subject_combo.setCurrentIndex(
                self.ui.subject_combo.findData(lesson.subject_id),
            )
            self.lesson_date = lesson.at.date()
            self.ui.time_edit.setTime(lesson.at.time())

            if lesson.note:
                self.ui.note_edit.setPlainText(lesson.note)

            if lesson.mark:
                self.ui.mark_spinbox.setValue(lesson.mark)
            self.ui.room_spinbox.setValue(lesson.room)
            self.ui.index_number_spinbox.setValue(lesson.index_number)

    def on_submit_btn(self) -> None:
        if not self.subject_id or not self.lesson_date or not self.lesson_time:
            return

        self.date_time = datetime.combine(self.lesson_date, self.lesson_time)

        with self.container() as r_container:
            if not self.lesson_id:
                data = NewLesson(
                    subject_id=self.subject_id,
                    at=self.date_time,
                    note=self.note,
                    mark=self.mark,
                    room=self.room,
                    index_number=self.index_number,
                )
                command = r_container.get(CreateLesson)
                command.execute(data)
            else:
                data_update = UpdatedLesson(
                    lesson_id=self.lesson_id,
                    subject_id=self.subject_id,
                    at=self.date_time,
                    note=self.note,
                    mark=self.mark,
                    room=self.room,
                    index_number=self.index_number,
                )
                command_update = r_container.get(UpdateLesson)
                command_update.execute(data_update)

        self.close()

    def on_delete_btn(self) -> None:
        if not self.lesson_id:
            return

        with self.container() as r_container:
            command = r_container.get(DeleteLesson)
            command.execute(self.lesson_id)

        self.close()

    def on_subject_combo_changed(self) -> None:
        self.subject_id = self.ui.subject_combo.currentData()

    def on_time_changed(self) -> None:
        self.lesson_time = self.ui.time_edit.time().toPyTime()

    def on_note_edit_changed(self) -> None:
        self.note = self.ui.note_edit.toPlainText()

    def on_mark_changed(self) -> None:
        self.mark = self.ui.mark_spinbox.value()

    def on_room_changed(self) -> None:
        self.room = self.ui.room_spinbox.value()

    def on_index_number_changed(self) -> None:
        self.index_number = self.ui.index_number_spinbox.value()

    def open_calendar_dialog(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор даты")

        layout = QVBoxLayout(dialog)

        calendar = QCalendarWidget(dialog)
        if self.lesson_date:
            calendar.setSelectedDate(self.lesson_date)
        layout.addWidget(calendar)

        confirm_button = QPushButton("Выбрать", dialog)
        confirm_button.clicked.connect(
            lambda: self.set_date_from_calendar(calendar, dialog),
        )
        layout.addWidget(confirm_button)

        dialog.setLayout(layout)
        dialog.exec()

    def set_date_from_calendar(
        self,
        calendar: QCalendarWidget,
        dialog: QDialog,
    ) -> None:
        self.lesson_date = calendar.selectedDate().toPyDate()
        dialog.accept()
