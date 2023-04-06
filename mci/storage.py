import pathlib

import requests

from mci import config


def download_file(id: int, url: str):
    extension = url.split(".")[-1]
    file = _get_storage_dir().joinpath(f"{id}.{extension}")
    with requests.get(url, stream=True) as response:
        with open(file) as f:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1 * 1024 * 1024):
                f.write(chunk)
    pass


def _get_storage_dir() -> pathlib.Path:
    storage_dir = config.storage_dir
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir
