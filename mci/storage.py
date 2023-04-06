import datetime

import filetype
import requests

from mci import config, db
import PIL.Image
import hashlib


def create_image(url: str):
    with db.get_connection() as c:
        image_id = db.create(c)
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
            width = pil_image.width
            height = pil_image.height

        path = str(file.relative_to(config.storage_dir))
        db.update_metadata(
            c=c,
            image_id=image_id,
            path=path,
            width=width,
            height=height,
            mimetype=type.mime,
            sha256hash=hash.hexdigest()
        )
    pass
