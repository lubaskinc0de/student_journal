from adaptix import Retort, loader, name_mapping

from student_journal.domain.home_task import HomeTask

home_task_retort = Retort(
    recipe=[
        loader(
            bool,
            lambda x: 1 if x is True else 0,
        ),
    ],
)
home_task_to_list_retort = Retort(
    recipe=[
        loader(
            bool,
            lambda x: 1 if x is True else 0,
        ),
        name_mapping(
            HomeTask,
            as_list=True,
        ),
    ],
)
