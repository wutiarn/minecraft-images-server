import os
import pathlib
import pytz

telegram_token = os.getenv("TELEGRAM_TOKEN")
storage_dir = pathlib.Path(os.getenv("STORAGE_DIR", "./storage"))
base_url = os.getenv("BASE_URL", "https://mci.wtrn.ru")
memos_url = os.getenv("MEMOS_URL", "http://192.168.31.3:5230")
telegram_user_whitelist = set([int(x) for x in os.getenv("TELEGRAM_USER_WHITELIST", "0").split(",")])

timezone = pytz.timezone("Europe/Moscow")
timestamp_format = "%Y-%m-%d %H:%M:%S %Z"

storage_dir.mkdir(parents=True, exist_ok=True)

