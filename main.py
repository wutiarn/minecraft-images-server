import logging
import logging
import os

import waitress as waitress
from flask import Flask, abort, request, redirect, send_file, stream_with_context, Response

from mci import memos
from mci.config import memos_public_url
from mci.db import migrations

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


@flask_app.route(f"/storage/i/<memo_id>", methods=["GET"])
def get_file(memo_id: int):
    token = _get_authorization_token()
    content = memos.get_memos_content(token, memo_id)
    content_image_resource = content.get_image_resource()
    if content_image_resource:
        resource_response = memos.get_resource(token, content_image_resource.id)
        return Response(stream_with_context(resource_response.iter_content(chunk_size=4096)), content_type = resource_response.headers['content-type'])
    return "TODO"

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
