from dishka import Provider, Scope, WithParents, from_context, provide

from student_journal.adapters.error_locator import ErrorLocator, SimpleErrorLocator
from student_journal.adapters.id_provider import FileStudentIdProvider
from student_journal.adapters.load_test_data import TestDataLoader
from student_journal.adapters.tz import SimpleTimezoneProvider, UserTimezone


class AdapterProvider(Provider):
    scope = Scope.REQUEST

    user_timezone = from_context(UserTimezone, scope=Scope.APP)
    id_provider = provide(WithParents[FileStudentIdProvider])
    error_locator = provide(
        source=SimpleErrorLocator,
        provides=ErrorLocator,
        scope=Scope.APP,
    )
    data_loader = provide(TestDataLoader)
    timezone_provider = provide(WithParents[SimpleTimezoneProvider], scope=Scope.APP)
