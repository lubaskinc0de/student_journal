import logging
import logging.config
from typing import Any

import structlog


def preprocessors() -> list[Any]:
    return [
        structlog.processors.dict_tracebacks,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.stdlib.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            },
        ),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]


def init_structlog() -> None:
    handlers = {
        "jsonformat": {
            "class": "logging.StreamHandler",
            "formatter": "jsonformat_formatter",
            "level": "DEBUG",
        },
    }

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "jsonformat_formatter": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(),
                    "foreign_pre_chain": preprocessors(),
                },
            },
            "handlers": handlers,
            "loggers": {
                "": {
                    "handlers": ["jsonformat"],
                    "level": "DEBUG",
                    "propagate": True,
                },
            },
        },
    )

    structlog.configure(
        processors=preprocessors(),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.getLogger().setLevel(logging.DEBUG)
