import os
import pathlib

telegram_token = os.getenv("TELEGRAM_TOKEN")
storage_dir = pathlib.Path(os.getenv("STORAGE_DIR", "./storage"))

storage_dir.mkdir(parents=True, exist_ok=True)
