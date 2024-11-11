import threading

from dishka import Container, make_container

from student_journal.adapters.config import Config, load_from_file
from student_journal.bootstrap.di.adapter_provider import AdapterProvider
from student_journal.bootstrap.di.command_provider import CommandProvider
from student_journal.bootstrap.di.config_provider import ConfigProvider
from student_journal.bootstrap.di.db_provider import DbProvider
from student_journal.bootstrap.di.gateway_provider import GatewayProvider


def get_container_for_gui() -> Container:
    config = load_from_file()

    return make_container(
        ConfigProvider(),
        CommandProvider(),
        AdapterProvider(),
        DbProvider(),
        GatewayProvider(),
        context={
            Config: config,
        },
        lock_factory=threading.Lock,
    )
