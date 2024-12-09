from dishka import Provider, Scope, provide

from student_journal.adapters.error_locator import ErrorLocator, SimpleErrorLocator
from student_journal.adapters.id_provider import FileStudentIdProvider
from student_journal.adapters.load_test_data import TestDataLoader
from student_journal.application.common.id_provider import StudentIdProvider


class AdapterProvider(Provider):
    scope = Scope.REQUEST

    id_provider = provide(source=FileStudentIdProvider, provides=StudentIdProvider)
    file_id_provider = provide(FileStudentIdProvider)
    error_locator = provide(
        source=SimpleErrorLocator,
        provides=ErrorLocator,
        scope=Scope.APP,
    )
    data_loader = provide(TestDataLoader)
