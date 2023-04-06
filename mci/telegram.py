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

    if file_id:
        storage.download_file(1, _get_file_download_url(file_id))


def _get_file_download_url(file_id: str):
    response = requests.get(f"{_base_methods_url}/getFile", params={"file_id": file_id})
    file_path = response.json()["result"]["file_path"]
    url = f"{_base_url}/file/bot{config.telegram_token}/{file_path}"
    return url
