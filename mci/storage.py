import datetime
import hashlib
from pathlib import Path
from sqlite3 import Connection

import PIL.ExifTags
import PIL.Image
import filetype
import requests

from mci import config, db, render
from mci.memos import MemosContent


def get_image_id(content: MemosContent):
    return content.id + "_" + hashlib.sha256(content.content).hexdigest()


def render_image(text: str, image_id: int, c: Connection):
    directory = _get_target_directory()
    file = directory.joinpath(f"{image_id}.png")
    render.render_image(text, file)
    path = str(file.relative_to(config.storage_dir))
    with PIL.Image.open(file) as image:
        width = image.width
        height = image.height
    db.update_image_metadata(
        c=c,
        image_id=image_id,
        path=path,
        width=width,
        height=height,
        mimetype="image/png",
        sha256hash=None
    )


def download_image(url: str, image_id: int, c: Connection):
    directory = _get_target_directory()
    file = directory.joinpath(f"{image_id}.tmp")
    hash = hashlib.sha256()
    with requests.get(url, stream=True) as response:
        with open(file, "wb") as f:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1 * 1024 * 1024):
                f.write(chunk)
                hash.update(chunk)
    type = filetype.guess(file)
    target_file = directory.joinpath(f"{image_id}.{type.extension}")
    file = file.rename(target_file)

    with PIL.Image.open(file) as pil_image:
        image = _rotate_by_exif(pil_image)
        width = image.width
        height = image.height

    path = str(file.relative_to(config.storage_dir))
    db.update_image_metadata(
        c=c,
        image_id=image_id,
        path=path,
        width=width,
        height=height,
        mimetype=type.mime,
        sha256hash=hash.hexdigest()
    )


def _get_target_directory() -> Path:
    now = datetime.datetime.now()
    directory = config.storage_dir.joinpath(str(now.year)).joinpath(f"{now.month:02}")
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _rotate_by_exif(image: PIL.Image):
    exif_orientation_tag_id = 274  # See PIL.ExifTags.TAGS
    exif_tags = image._getexif()
    if not exif_tags or exif_orientation_tag_id not in exif_tags:
        return image

    rotation_tag_value = exif_tags[exif_orientation_tag_id]
    if rotation_tag_value == 6:
        return image.rotate(90, expand=True)
    elif rotation_tag_value == 3:
        return image.rotate(180, expand=True)
    elif rotation_tag_value == 8:
        return image.rotate(270, expand=True)
    else:
        return image
