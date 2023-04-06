from mci import storage, config

_base_url = "https://api.telegram.org"


def handle_event(event: dict):
    if not "message" in event:
        return
    message = event["message"]

    file_id = None
    if "document" in message:
        file_id = message["document"]["file_id"]

    if file_id:
        _download_file(file_id)


def _download_file(file_id):
    url = f"{_base_url}/file/bot{config.telegram_token}/{file_id}"
    storage.download_file(1, url)
