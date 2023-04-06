import logging

from flask import Flask, abort
from mci import config
import secrets

flask_app = Flask(__name__)


@flask_app.route(f"/tg/hook/<token>")
def handle_telegram_hook(token: str):
    if not secrets.compare_digest(token, config.telegram_token):
        return abort(404)
    return "OK"


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s - %(message)s")
    flask_app.run(debug=True, host="0.0.0.0", port=8080)

