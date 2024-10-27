from adaptix import Retort, name_mapping

from student_journal.domain.teacher import Teacher

teacher_retort = Retort()
teacher_to_list_retort = Retort(
    recipe=[
        name_mapping(
            Teacher,
            as_list=True,
        ),
    ],
)
teachers_to_list_retort = Retort(
    recipe=[
        name_mapping(
            Teacher,
            as_list=True,
        ),
    ],
)
