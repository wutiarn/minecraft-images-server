import sqlite3

from mci import config

_DATABASE_LOCATION = config.storage_dir.joinpath("db.sqlite")


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(_DATABASE_LOCATION)
