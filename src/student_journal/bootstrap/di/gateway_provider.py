from dishka import Provider, Scope, WithParents, provide_all

from student_journal.adapters.db.gateway.home_task_gateway import SQLiteHomeTaskGateway
from student_journal.adapters.db.gateway.lesson_gateway import SQLiteLessonGateway
from student_journal.adapters.db.gateway.student_gateway import SQLiteStudentGateway
from student_journal.adapters.db.gateway.subject_gateway import SQLiteSubjectGateway
from student_journal.adapters.db.gateway.teacher_gateway import SQLiteTeacherGateway


class GatewayProvider(Provider):
    scope = Scope.REQUEST
    gateways = provide_all(
        WithParents[SQLiteStudentGateway],
        WithParents[SQLiteTeacherGateway],
        WithParents[SQLiteSubjectGateway],
        WithParents[SQLiteLessonGateway],
        WithParents[SQLiteHomeTaskGateway],
    )
