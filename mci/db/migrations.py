import logging

from yoyo import read_migrations, get_backend

from mci.db import DATABASE_LOCATION

logger = logging.getLogger("db.migrations")


def apply_migrations():
    backend = get_backend(f'sqlite:///{DATABASE_LOCATION}')
    migrations = read_migrations('migrations')
    with backend.lock():
        to_apply = backend.to_apply(migrations)
        backend.apply_migrations(to_apply)
