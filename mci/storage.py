import pathlib
from mci import config


def download_file(id: int, url: str):
    extension = url.split(".")[-1]
    file = _get_storage_dir().joinpath(f"{id}.{extension}")
    pass


def _get_storage_dir() -> pathlib.Path:
    storage_dir = config.storage_dir
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir
