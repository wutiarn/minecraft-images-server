import datetime
import logging
import secrets

from flask import Flask, abort, request, send_file, render_template

from mci import config, telegram, db
from mci.db import migrations
from mci.db.model import ImageStatus, ImageMetadata

flask_app = Flask(__name__)

logger = logging.getLogger("main")


@flask_app.route(f"/tg/hook/<token>", methods=["POST"])
def handle_telegram_hook(token: str):
    if not secrets.compare_digest(token, config.telegram_token):
        return abort(404)
    logger.info(f"Received webhook: {request.data.decode()}")
    telegram.handle_event(request.json)
    return "OK"


@flask_app.route(f"/i/<image_id>", methods=["GET"])
def get_metadata_page(image_id: int):
    image = _get_image(image_id)
    date = datetime.datetime.fromtimestamp(image.created_at)\
        .astimezone(config.timezone)\
        .strftime(config.timestamp_format)
    url = _get_storage_url(image)
    return render_template("image.html", image=image, date=date, url=url)


@flask_app.route(f"/i/<image_id>/meta.json", methods=["GET"])
def get_metadata_json(image_id: int):
    image = _get_image(image_id)
    url = _get_storage_url(image)
    return {
        "id": image.id,
        "url": url,
        "created_at": image.created_at,
        "width": image.width,
        "height": image.height,
        "mimetype": image.mimetype,
        "sha256hash": image.sha256hash
    }


@flask_app.route(f"/storage/i/<filename>", methods=["GET"])
def get_file(filename: str):
    image_id = int(filename.split(".")[0])
    image = _get_image(image_id)
    file = config.storage_dir.joinpath(image.path)
    return send_file(file, mimetype=image.mimetype, download_name=filename)


def _get_image(image_id: int) -> ImageMetadata:
    with db.get_connection() as c:
        image = db.load_image(c, image_id)
    if image.status != ImageStatus.OK:
        raise abort(404)
    return image

def _get_storage_url(image: ImageMetadata):
    extension = image.path.split(".")[-1]
    return f"{config.base_url}/storage/i/{image.id}.{extension}"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s - %(message)s")
    migrations.apply_migrations()
    flask_app.run(debug=True, host="0.0.0.0", port=8080)
