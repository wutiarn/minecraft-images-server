import os
import pathlib

storage_dir = pathlib.Path(os.getenv("STORAGE_DIR", "./storage"))
base_url = os.getenv("BASE_URL", "https://mci.wtrn.ru")
memos_url = os.getenv("MEMOS_URL", "http://192.168.31.3:5230")
memos_public_url = os.getenv("MEMOS_PUBLIC_URL", memos_url)
