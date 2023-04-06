import sqlite3

from mci import config

DATABASE_LOCATION = config.storage_dir.joinpath("db.sqlite").absolute()


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_LOCATION)
