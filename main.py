import datetime
import logging
import os
import secrets

import waitress as waitress
from flask import Flask, abort, request, send_file, render_template

from mci import config, telegram, db, memos
from mci.db import migrations
from mci.db.model import ImageStatus, ImageMetadata

flask_app = Flask(__name__)

logger = logging.getLogger("main")
_storage_base_url = "/storage/i"


@flask_app.route(f"/tg/hook/<token>", methods=["POST"])
def handle_telegram_hook(token: str):
    if not secrets.compare_digest(token, config.telegram_token):
        return abort(404)
    logger.info(f"Received webhook: {request.data.decode()}")
    try:
        telegram.handle_event(request.json)
    except Exception:
        logger.error("Failed to handle webhook", exc_info=True)
    return "OK"


@flask_app.route(f"/i/<image_id>", methods=["GET"])
def get_metadata_page(image_id: int):
    image = _get_image(image_id)
    date = datetime.datetime.fromtimestamp(image.created_at) \
        .astimezone(config.timezone) \
        .strftime(config.timestamp_format)
    url = _get_storage_url(image_id)
    return render_template("image.html", image=image, date=date, storage_url=url)


@flask_app.route(f"/i/<memo_id>/meta.json", methods=["GET"])
def get_metadata_json(memo_id):
    if memo_id == "latest":
        memo_id = None
    else:
        try:
            memo_id = int(memo_id)
        except ValueError:
            abort(400, "Failed to parse memo id " + memo_id)
    return memos.get_memos_metadata(_get_authorization_token(), memo_id).to_dict()
    # image = _get_image(image_id)
    # url = f"{config.base_url}{_get_storage_url(image_id)}"
    # return {
    #     "id": image.id,
    #     "url": url,
    #     "created_at": image.created_at,
    #     "width": image.width,
    #     "height": image.height,
    #     "mimetype": image.mimetype,
    #     "sha256hash": image.sha256hash,
    #     "description": image.text
    # }


@flask_app.route(f"{_storage_base_url}/<image_id>", methods=["GET"])
def get_file(image_id: int):
    image = _get_image(image_id)
    file = config.storage_dir.joinpath(image.path)
    extension = image.path.split(".")[-1]
    return send_file(file, mimetype=image.mimetype, download_name=f"{image_id}.{extension}")


def _get_image(image_id: int) -> ImageMetadata:
    with db.get_connection() as c:
        if image_id == "latest":
            image = db.load_latest_image(c)
        else:
            image = db.load_image(c, image_id)
    if not image:
        abort(404)
    if image.status != ImageStatus.OK:
        raise abort(404)
    return image


def _get_storage_url(image_id: int):
    return f"{_storage_base_url}/{image_id}"

def _get_authorization_token():
    header = request.headers.get("Authorization")
    if not header:
        abort(401, "No authorization header present")
    return header.replace("Bearer ", "")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s - %(message)s")
    migrations.apply_migrations()
    if os.getenv("DEV"):
        flask_app.run(debug=True, host="0.0.0.0", port=8801)
    else:
        waitress.serve(flask_app)
