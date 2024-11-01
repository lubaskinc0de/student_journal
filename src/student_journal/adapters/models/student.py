from adaptix import Retort, name_mapping

from student_journal.domain.student import Student

student_retort = Retort()
student_to_list_retort = Retort(
    recipe=[
        name_mapping(
            Student,
            as_list=True,
        ),
    ],
)
