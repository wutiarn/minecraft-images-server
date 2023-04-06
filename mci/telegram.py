import requests

from mci import storage, config

_base_url = "https://api.telegram.org"
_base_methods_url = f"{_base_url}/bot{config.telegram_token}"


def handle_event(event: dict):
    if not "message" in event:
        return
    message = event["message"]

    file_id = None
    if "document" in message:
        file_id = message["document"]["file_id"]

    if "photo" in message:
        file_id = _get_max_photo_resolution_file_id(message["photo"])

    if file_id:
        storage.download_file(1, _get_file_download_url(file_id))


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
