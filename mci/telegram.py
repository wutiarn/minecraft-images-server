import logging

import requests

from mci import storage, config

_base_url = "https://api.telegram.org"
_base_methods_url = f"{_base_url}/bot{config.telegram_token}"

logger = logging.getLogger("mci.telegram")


def handle_event(event: dict):
    if not "message" in event:
        return
    message = event["message"]

    from_id = message["from"]["id"]
    chat_id = message["chat"]["id"]
    message_id = message["message_id"]
    if from_id not in config.telegram_user_whitelist:
        send_message(
            chat=chat_id,
            reply_message_id=message_id,
            text=f"User {from_id} is not whitelisted"
        )
        return

    file_id = None
    if "document" in message:
        file_id = message["document"]["file_id"]

    if "photo" in message:
        file_id = _get_max_photo_resolution_file_id(message["photo"])

    if file_id:
        image_id = storage.create_image(_get_file_download_url(file_id))
        send_message(
            chat=message["chat"]["id"],
            reply_message_id=message["message_id"],
            text=f"Uploaded image id: #{image_id}\n{config.base_url}/i/{image_id}"
        )


def _get_file_download_url(file_id: str) -> str:
    response = requests.get(f"{_base_methods_url}/getFile", params={"file_id": file_id})
    file_path = response.json()["result"]["file_path"]
    url = f"{_base_url}/file/bot{config.telegram_token}/{file_path}"
    return url


def _get_max_photo_resolution_file_id(photos: list[dict]) -> str:
    max_file_size = 0
    file_id = None
    for photo in photos:
        file_size = photo["file_size"]
        if file_size > max_file_size:
            max_file_size = file_size
            file_id = photo["file_id"]
    return file_id


def send_message(chat: int, text: str, reply_message_id: int):
    data = {
        "chat_id": chat,
        "text": text
    }
    if reply_message_id:
        data["reply_to_message_id"] = reply_message_id
    response = requests.post(f"{_base_methods_url}/sendMessage", data=data)
    if response.status_code != 200:
        logger.warning(f"Failed to send message: telegram returned {response.text}")
