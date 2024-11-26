from dishka import Container
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QWidget

from student_journal.application.models.subject import SubjectReadModel
from student_journal.application.subject.read_subjects import ReadSubjects
from student_journal.presentation.ui.progress_ui import Ui_Progress


class Progress(QWidget):
    def __init__(self, container: Container) -> None:
        super().__init__()
        self.container = container
        self.ui = Ui_Progress()
        self.ui.setupUi(self)

        self.ui.refresh.clicked.connect(self.on_refresh)
        self.ui.sorting.currentIndexChanged.connect(self.on_sort_changed)
        self.ui.show_without_mark.stateChanged.connect(self.on_toggle_without_mark)

        self.load_subjects()

    def load_subjects(self) -> None:
        show_without_mark = not self.ui.show_without_mark.isChecked()
        sort_by_title = False
        sort_by_avg_mark = False
        sorting_index = self.ui.sorting.currentIndex()

        if sorting_index == 0:
            sort_by_title = True
        elif sorting_index == 1:
            sort_by_avg_mark = True

        with self.container() as r_container:
            command = r_container.get(ReadSubjects)
            subjects = command.execute(
                sort_by_title=sort_by_title,
                sort_by_avg_mark=sort_by_avg_mark,
                show_empty=show_without_mark,
            )
        self.populate_table(subjects)

    def populate_table(self, subjects: list[SubjectReadModel]) -> None:
        self.ui.table.setRowCount(len(subjects))
        for row, subject in enumerate(subjects):
            self.ui.table.setItem(row, 0, QTableWidgetItem(subject.title))
            avg_mark_item = QTableWidgetItem(
                f"{subject.avg_mark:.2f}" if subject.avg_mark != 0.0 else "—",
            )
            avg_mark_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.table.setItem(row, 1, avg_mark_item)

            marks_list_item = QTableWidgetItem(
                f"{' '.join(map(str, subject.marks_list))}"
                if subject.marks_list else "—",
            )
            self.ui.table.setItem(row, 2, marks_list_item)

    def on_refresh(self) -> None:
        self.load_subjects()

    def on_sort_changed(self) -> None:
        self.load_subjects()

    def on_toggle_without_mark(self) -> None:
        self.load_subjects()

