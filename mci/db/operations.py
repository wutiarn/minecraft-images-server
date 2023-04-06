import sqlite3
import time

from mci.db import DATABASE_LOCATION
from mci.db.model import ImageStatus


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_LOCATION)


def create(c: sqlite3.Connection) -> int:
    result = c.execute("INSERT INTO images (status, created_at) values (:status, :created_at) RETURNING (id)",
                       {"status": ImageStatus.PENDING.value, "created_at": int(time.time())})
    returned = result.fetchone()
    return returned[0]
