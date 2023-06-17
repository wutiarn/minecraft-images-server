import sqlite3
import time

from mci.db import DATABASE_LOCATION
from mci.db.model import ImageStatus, ImageMetadata


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_LOCATION)


def create(c: sqlite3.Connection, from_id: int, message_compound_id: str, text: str) -> int:
    result = c.execute(
        "INSERT INTO images (status, created_at, from_id, message_compound_id, text) "
        "values (:status, :created_at, :from_id, :message_compound_id, :text) RETURNING (id)",
        {
            "status": ImageStatus.PENDING.value,
            "created_at": int(time.time()),
            "from_id": from_id,
            "message_compound_id": message_compound_id,
            "text": text
        })
    returned = result.fetchone()
    c.commit()
    return returned[0]


def edit_message_details(c: sqlite3.Connection, message_compound_id: str, text: str) -> int | None:
    result = c.execute(
        "UPDATE images SET text = :text WHERE message_compound_id = :message_compound_id RETURNING (id);",
        {
            "message_compound_id": message_compound_id,
            "text": text
        })
    returned = result.fetchone()
    c.commit()
    if not returned:
        return None
    return returned[0]


def update_image_metadata(
        c: sqlite3.Connection,
        image_id: int,
        path: str,
        width: int,
        height: int,
        mimetype: str,
        sha256hash: str | None
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
                       "id, "
                       "status, "
                       "created_at, "
                       "text, "
                       "path, "
                       "width, "
                       "height, "
                       "mimetype, "
                       "sha256hash "
                       "FROM images WHERE id = :id", {"id": image_id})
    row = result.fetchone()
    if not row:
        return None

    return ImageMetadata.from_row(row)


def load_latest_image(c: sqlite3.Connection):
    result = c.execute("SELECT "
                       "id, "
                       "status, "
                       "created_at, "
                       "text, "
                       "path, "
                       "width, "
                       "height, "
                       "mimetype, "
                       "sha256hash "
                       "FROM images "
                       "ORDER BY id DESC "
                       "LIMIT 1")
    row = result.fetchone()
    if not row:
        return None

    return ImageMetadata.from_row(row)
