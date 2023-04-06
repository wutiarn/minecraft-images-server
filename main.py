import logging

from flask import Flask, abort, request
from mci import config, telegram
from mci.db import migrations
import secrets

flask_app = Flask(__name__)

logger = logging.getLogger("main")


@flask_app.route(f"/tg/hook/<token>", methods=["POST"])
def handle_telegram_hook(token: str):
    if not secrets.compare_digest(token, config.telegram_token):
        return abort(404)
    logger.info(f"Received webhook: {request.data.decode()}")
    telegram.handle_event(request.json)
    return "OK"


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s - %(message)s")
    migrations.apply_migrations()
    flask_app.run(debug=True, host="0.0.0.0", port=8080)
