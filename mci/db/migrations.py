from yoyo import read_migrations
from yoyo import get_backend
from mci.db import operations

backend = get_backend(f'sqlite://{operations.DATABASE_LOCATION}')
migrations = read_migrations('migrations')


def apply_migrations():
    with backend.lock():
        to_apply = backend.to_apply(migrations)
        backend.apply_migrations(to_apply)
