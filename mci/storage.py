import datetime
import hashlib

import PIL.Image
import PIL.ExifTags
import filetype
import requests

from mci import config, db


def download_image(url: str, image_id: int):
    with db.get_connection() as c:
        now = datetime.datetime.now()
        directory = config.storage_dir.joinpath(str(now.year)).joinpath(f"{now.month:02}")
        directory.mkdir(parents=True, exist_ok=True)
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
