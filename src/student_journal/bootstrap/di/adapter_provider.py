from dishka import Provider, Scope, provide

from student_journal.adapters.error_locator import ErrorLocator, SimpleErrorLocator
from student_journal.adapters.id_provider import FileIdProvider
from student_journal.adapters.load_test_data import TestDataLoader
from student_journal.application.common.id_provider import IdProvider


class AdapterProvider(Provider):
    scope = Scope.REQUEST

    id_provider = provide(source=FileIdProvider, provides=IdProvider)
    file_id_provider = provide(FileIdProvider)
    error_locator = provide(
        source=SimpleErrorLocator,
        provides=ErrorLocator,
        scope=Scope.APP,
    )
    data_loader = provide(TestDataLoader)
