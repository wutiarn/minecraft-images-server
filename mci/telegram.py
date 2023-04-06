def handle_event(event: dict):
    if not "message" in event:
        return
    message = event["message"]

    file_id = None
    if "document" in message:
        file_id = message["document"]["file_id"]
    pass

