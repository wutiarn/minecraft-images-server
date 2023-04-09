from dataclasses import dataclass
from enum import Enum

from dataclasses_json import dataclass_json


class ImageStatus(Enum):
    PENDING = 1
    OK = 2
    DELETED = 3


@dataclass_json
@dataclass
class ImageMetadata:
    id: int
    status: ImageStatus
    created_at: int
    text: str
    path: str
    width: int
    height: int
    mimetype: str
    sha256hash: str
