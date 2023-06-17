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

    @staticmethod
    def from_row(row):
        return ImageMetadata(
            id=row[0],
            status=ImageStatus(row[1]),
            created_at=row[2],
            text=row[3],
            path=row[4],
            width=row[5],
            height=row[6],
            mimetype=row[7],
            sha256hash=row[8]
        )
