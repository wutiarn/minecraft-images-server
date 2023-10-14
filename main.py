import logging
import os

import waitress as waitress
from flask import Flask, abort, request, stream_with_context, Response, send_file

from mci import memos, storage

flask_app = Flask(__name__)

logger = logging.getLogger("main")


@flask_app.route(f"/i/<memo_id>/meta.json", methods=["GET"])
def get_metadata_json(memo_id):
    if memo_id == "latest":
        memo_id = None
    else:
        try:
            memo_id = int(memo_id)
        except ValueError:
            abort(400, "Failed to parse memo id " + memo_id)
    return memos.get_memos_minecraft_metadata(_get_authorization_token(), memo_id).to_dict()


@flask_app.route(f"/storage/i/<memo_id>", methods=["GET"])
def get_file(memo_id: int):
    token = _get_authorization_token()
    content = memos.get_memos_content(token, memo_id)
    content_image_resource = content.get_image_resource()
    if content_image_resource:
        resource_response = memos.get_resource(token, content_image_resource.id)
        return Response(stream_with_context(resource_response.iter_content(chunk_size=4096)),
                        content_type=resource_response.headers['content-type'])
    file = storage.get_image_file(content)
    return send_file(file, "image/png")


def _get_authorization_token():
    header = request.headers.get("Authorization")
    if not header:
        abort(401, "No authorization header present")
    return header.replace("Bearer ", "")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s - %(message)s")
    if os.getenv("DEV"):
        flask_app.run(debug=True, host="0.0.0.0", port=8801)
    else:
        waitress.serve(flask_app)
