from adaptix import Retort, name_mapping

from student_journal.application.models.lesson import WeekLessons
from student_journal.domain.lesson import Lesson

lesson_retort = Retort()
lesson_to_list_retort = Retort(
    recipe=[
        name_mapping(
            Lesson,
            as_list=True,
        ),
    ],
)
lessons_to_list_retort = Retort(
    recipe=[
        name_mapping(
            WeekLessons,
            as_list=True,
        ),
    ],
)
