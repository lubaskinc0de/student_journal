from datetime import datetime

from adaptix import Retort, dumper, loader, name_mapping

from student_journal.application.models.lesson import WeekLessons
from student_journal.domain.lesson import Lesson

lesson_retort = Retort()
lesson_to_list_retort = Retort(
    recipe=[
        loader(datetime, lambda x: x),
        dumper(datetime, lambda x: x),
        name_mapping(
            Lesson,
            as_list=True,
        ),
    ],
)
lessons_to_list_retort = Retort(
    recipe=[
        loader(datetime, lambda x: x),
        dumper(datetime, lambda x: x),
        name_mapping(
            WeekLessons,
            as_list=True,
        ),
    ],
)
