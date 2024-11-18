from dishka import Provider, Scope, provide

from student_journal.adapters.db.gateway.home_task_gateway import SQLiteHomeTaskGateway
from student_journal.adapters.db.gateway.lesson_gateway import SQLiteLessonGateway
from student_journal.adapters.db.gateway.student_gateway import SQLiteStudentGateway
from student_journal.adapters.db.gateway.subject_gateway import SQLiteSubjectGateway
from student_journal.adapters.db.gateway.teacher_gateway import SQLiteTeacherGateway
from student_journal.application.common.home_task_gateway import HomeTaskGateway
from student_journal.application.common.lesson_gateway import LessonGateway
from student_journal.application.common.student_gateway import StudentGateway
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.teacher_gateway import TeacherGateway


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    student_gateway = provide(SQLiteStudentGateway, provides=StudentGateway)
    teacher_gateway = provide(SQLiteTeacherGateway, provides=TeacherGateway)
    subject_gateway = provide(SQLiteSubjectGateway, provides=SubjectGateway)
    lesson_gateway = provide(SQLiteLessonGateway, provides=LessonGateway)
    home_task_gateway = provide(SQLiteHomeTaskGateway, provides=HomeTaskGateway)
