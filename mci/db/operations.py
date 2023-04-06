import sqlite3
import time

from mci.db import DATABASE_LOCATION
from mci.db.model import ImageStatus, ImageMetadata


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


def load_image(c: sqlite3.Connection, image_id: int):
    result = c.execute("SELECT "
                    "status, "
                    "created_at, "
                    "path, "
                    "width, "
                    "height, "
                    "mimetype, "
                    "sha256hash "
                    "FROM images WHERE id = :id", {"id": image_id})
    row = result.fetchone()

    return ImageMetadata(
        id=image_id,
        status=row[0],
        created_at=row[1],
        path=row[2],
        width=row[3],
        height=row[4],
        mimetype=row[5],
        sha256hash=row[6]
    )
