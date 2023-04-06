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
    c.commit()
    return returned[0]


def update_metadata(
        c: sqlite3.Connection,
        image_id: int,
        path: str,
        width: int,
        height: int,
        mimetype: str,
        sha256hash: str
):
    c.execute("UPDATE images "
              "SET status = :status,"
              "path = :path, "
              "width = :width, "
              "height = :height, "
              "mimetype = :mimetype, "
              "sha256hash = :sha256hash "
              "WHERE id = :image_id", {
                  "image_id": image_id,
                  "status": ImageStatus.OK.value,
                  "path": path,
                  "width": width,
                  "height": height,
                  "mimetype": mimetype,
                  "sha256hash": sha256hash
              })
    c.commit()
