from dataclasses import dataclass
from datetime import timezone
from typing import NewType

from student_journal.application.common.tz import TimezoneProvider

UserTimezone = NewType("UserTimezone", timezone)


@dataclass(slots=True, frozen=True)
class SimpleTimezoneProvider(TimezoneProvider):
    tz: UserTimezone

    def get_timezone(self) -> timezone:
        return self.tz
