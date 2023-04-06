import json
import logging

from flask import Flask, abort, request
from mci import config, telegram, db
from mci.db import migrations
import secrets
from dataclasses_json import dataclass_json

from mci.db.model import ImageStatus

flask_app = Flask(__name__)

logger = logging.getLogger("main")


@flask_app.route(f"/tg/hook/<token>", methods=["POST"])
def handle_telegram_hook(token: str):
    if not secrets.compare_digest(token, config.telegram_token):
        return abort(404)
    logger.info(f"Received webhook: {request.data.decode()}")
    telegram.handle_event(request.json)
    return "OK"


@flask_app.route(f"/i/<image_id>/meta.json", methods=["GET"])
def get_metadata(image_id: int):
    with db.get_connection() as c:
        image = db.load_image(c, image_id)
    if image.status != ImageStatus.OK:
        return abort(404)
    extension = image.path.split(".")[-1]
    url = f"{config.base_url}/storage/i/{image_id}.{extension}"
    return {
        "id": image.id,
        "url": url,
        "created_at": image.created_at,
        "width": image.width,
        "height": image.height,
        "mimetype": image.mimetype,
        "sha256hash": image.sha256hash
    }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s - %(message)s")
    migrations.apply_migrations()
    flask_app.run(debug=True, host="0.0.0.0", port=8080)
