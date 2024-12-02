from dishka import Provider, Scope, provide_all

from student_journal.application.hometask.create_home_task import CreateHomeTask
from student_journal.application.hometask.delete_home_task import DeleteHomeTask
from student_journal.application.hometask.read_home_task import ReadHomeTask
from student_journal.application.hometask.read_home_tasks import ReadHomeTasks
from student_journal.application.hometask.update_home_task import UpdateHomeTask
from student_journal.application.lesson.create_lesson import CreateLesson
from student_journal.application.lesson.delete_all_lessons import DeleteAllLessons
from student_journal.application.lesson.delete_lesson import DeleteLesson
from student_journal.application.lesson.delete_lessons_for_week import (
    DeleteLessonsForWeek,
)
from student_journal.application.lesson.read_first_lessons_of_weeks import (
    ReadFirstLessonsOfWeeks,
)
from student_journal.application.lesson.read_lesson import ReadLesson
from student_journal.application.lesson.read_lessons_for_week import ReadLessonsForWeek
from student_journal.application.lesson.update_lesson import UpdateLesson
from student_journal.application.student.create_student import CreateStudent
from student_journal.application.student.read_student import ReadStudent
from student_journal.application.student.update_student import UpdateStudent
from student_journal.application.subject.create_subject import CreateSubject
from student_journal.application.subject.delete_subject import DeleteSubject
from student_journal.application.subject.read_subject import ReadSubject
from student_journal.application.subject.read_subjects import ReadSubjects
from student_journal.application.subject.update_subject import UpdateSubject
from student_journal.application.teacher import (
    CreateTeacher,
    DeleteTeacher,
    ReadTeacher,
    ReadTeachers,
    UpdateTeacher,
)


class CommandProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        CreateStudent,
        ReadStudent,
        UpdateStudent,
        CreateTeacher,
        DeleteTeacher,
        ReadTeacher,
        ReadTeachers,
        UpdateTeacher,
        CreateSubject,
        DeleteSubject,
        ReadSubject,
        ReadSubjects,
        UpdateSubject,
        CreateLesson,
        DeleteLesson,
        ReadFirstLessonsOfWeeks,
        ReadLesson,
        ReadLessonsForWeek,
        UpdateLesson,
        CreateHomeTask,
        DeleteHomeTask,
        ReadHomeTask,
        ReadHomeTasks,
        UpdateHomeTask,
        DeleteLessonsForWeek,
        DeleteAllLessons,
    )
