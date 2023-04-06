import logging

from yoyo import read_migrations, get_backend

from mci.db import operations

logger = logging.getLogger("db.migrations")


def apply_migrations():
    # _create_db()
    backend = get_backend(f'sqlite:///{operations.DATABASE_LOCATION}')
    migrations = read_migrations('migrations')
    with backend.lock():
        to_apply = backend.to_apply(migrations)
        backend.apply_migrations(to_apply)
