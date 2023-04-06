from mci import config as _config

DATABASE_LOCATION = _config.storage_dir.joinpath("db.sqlite3").absolute()

from mci.db.operations import get_connection, create, update_metadata
