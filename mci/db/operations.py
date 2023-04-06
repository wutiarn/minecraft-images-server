import sqlite3
import time

from mci import config
from mci.db.model import ImageStatus

DATABASE_LOCATION = config.storage_dir.joinpath("db.sqlite3").absolute()


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_LOCATION)


def create(c: sqlite3.Connection) -> int:
    result = c.execute("INSERT INTO images (status, created_at) values (:status, :created_at)",
                        parameters={"status": ImageStatus.PENDING, "created_at": time.time()})
    created = result.fetchone()
    return 0
