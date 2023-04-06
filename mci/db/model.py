from dataclasses import dataclass
from enum import Enum


class ImageStatus(Enum):
    PENDING = 1
    OK = 2
    DELETED = 3


@dataclass
class ImageMetadata:
    id: int
    status: ImageStatus
    created_at: int
    path: str
    width: int
    height: int
    mimetype: str
    sha256hash: str
