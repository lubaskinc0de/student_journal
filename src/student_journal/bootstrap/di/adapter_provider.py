from dishka import Provider, Scope, provide

from student_journal.adapters.id_provider import FileIdProvider
from student_journal.application.common.id_provider import IdProvider


class AdapterProvider(Provider):
    scope = Scope.REQUEST

    id_provider = provide(source=FileIdProvider, provides=IdProvider, scope=Scope.APP)
