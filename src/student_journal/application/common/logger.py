from typing import NewType

import structlog
from adaptix import Retort

Logger = NewType("Logger", structlog.stdlib.BoundLogger)
retort = Retort()
