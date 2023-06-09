import logging

import requests

from mci import storage, config, db

_base_url = "https://api.telegram.org"
_base_methods_url = f"{_base_url}/bot{config.telegram_token}"

logger = logging.getLogger("mci.telegram")


def handle_event(event: dict):
    message: dict = event.get("message")
    is_edit = False
    if not message:
        message = event.get("edited_message")
        is_edit = True
    if not message:
        return

    from_id = message["from"]["id"]
    chat_id = message["chat"]["id"]
    message_id = message["message_id"]

    text = message.get("caption")

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
        image_id = _handle_message(
            from_id=from_id,
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            file_id=file_id
        )
        if not is_edit:
            send_message(
                chat=chat_id,
                reply_message_id=message_id,
                text=f"Image uploaded: #{image_id}\n{config.base_url}/i/{image_id}"
            )
        else:
            send_message(
                chat=chat_id,
                reply_message_id=message_id,
                text=f"Image #{image_id} edited\n{config.base_url}/i/{image_id}"
            )


def _handle_message(from_id: int, chat_id: int, message_id: int, text: str, file_id: str) -> int:
    message_compound_id = f"{chat_id}_{message_id}"
    with db.get_connection() as c:
        image_id = db.edit_message_details(c, message_compound_id=message_compound_id, text=text)
        if image_id is None:
            image_id = db.create(c, from_id=from_id, message_compound_id=message_compound_id, text=text)
        storage.download_image(
            url=_get_file_download_url(file_id),
            image_id=image_id
        )
        return image_id


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
