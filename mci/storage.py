import hashlib
import os.path
from pathlib import Path

from mci import config, render
from mci.memos import MemosContent


def get_image_file(content: MemosContent) -> Path:
    file_name = f"{content.id}_{content.updated_at}.png"
    file = _get_target_file(file_name)
    if file.exists() and os.path.getsize(file) > 0:
        return file
    render.render_image(content.content, file)
    return file


def _get_target_file(file_name: str) -> Path:
    file_name_hash = hashlib.sha256(file_name.encode()).hexdigest()
    directory = config.storage_dir.joinpath("render_cache").joinpath(file_name_hash[:2])
    directory.mkdir(parents=True, exist_ok=True)
    return directory.joinpath(file_name)
