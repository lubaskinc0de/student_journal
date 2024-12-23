from datetime import time

from student_journal.application.invariants.lesson import (
    MIN_ROOM,
    MAX_MARK,
)
from student_journal.presentation.ui.raw.edit_lesson_ui import Ui_EditLesson


class EditLessonUI(Ui_EditLesson):
    def setupUi(self, *args, **kwargs):
        super().setupUi(*args, **kwargs)
        self.set_invariants()

    def set_invariants(self):
        self.room_spinbox.setMinimum(MIN_ROOM)
        self.room_spinbox.setMaximum(1_000_000)
        self.mark_spinbox.setMinimum(0)

        self.mark_spinbox.setValue(0)
        self.mark_spinbox.setSpecialValueText("Не выбрано")
        self.mark_spinbox.setMaximum(MAX_MARK)

        default_time = time(hour=8, minute=0, second=0)
        self.time_edit.setMinimumTime(default_time)
        self.datetime_preview.setTime(default_time)
