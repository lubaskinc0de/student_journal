from dataclasses import dataclass
from pathlib import Path

from student_journal.adapters.db.connection_maker import DBConfig
from student_journal.adapters.id_provider import CredentialsConfig

BASE_PATH = Path(Path.expanduser(Path("~/student_journal/")))
CREDENTIALS_PATH = Path(BASE_PATH / "auth.toml")


@dataclass(slots=True, frozen=True)
class Config:
    db: DBConfig
    credentials: CredentialsConfig


def load_from_file() -> Config:
    if not BASE_PATH.exists():
        BASE_PATH.mkdir(parents=True)

    return Config(
        db=DBConfig(
            db_path=str(BASE_PATH / "db.sqlite3"),
        ),
        credentials=CredentialsConfig(
            path=CREDENTIALS_PATH,
        ),
    )
