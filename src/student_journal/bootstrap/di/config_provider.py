from dishka import Provider, Scope, from_context, provide

from student_journal.adapters.config import Config
from student_journal.adapters.db.connection_maker import DBConfig
from student_journal.adapters.id_provider import CredentialsConfig


class ConfigProvider(Provider):
    scope = Scope.APP
    config = from_context(provides=Config, scope=Scope.APP)

    @provide()
    def db_config(self, config: Config) -> DBConfig:
        return config.db

    @provide()
    def credentials_config(self, config: Config) -> CredentialsConfig:
        return config.credentials
