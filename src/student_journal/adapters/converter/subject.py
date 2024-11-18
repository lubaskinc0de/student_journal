from adaptix import Retort, name_mapping

from student_journal.domain.subject import Subject

subject_retort = Retort()
subject_to_list_retort = Retort(
    recipe=[
        name_mapping(
            Subject,
            as_list=True,
        ),
    ],
)
