from dataclasses import dataclass

import requests
from dataclasses_json import dataclass_json, LetterCase

from mci.config import memos_url


def get_memos_content(token: str, memo_id: int):
    response = requests.get(f"{memos_url}/api/v1/memo/{memo_id}", headers=_build_headers(token))
    return MemosContent.from_dto(response.json())


def _build_headers(token: str):
    return {
        "Authorization": "Bearer " + token
    }


@dataclass
class MemosResource:
    id: int
    type: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MemosContent:
    creator_username: str
    content: str
    resources: list[MemosResource]

    @staticmethod
    def from_dto(dto: dict):
        resources = []
        for res_dto in dto.get("resourceList", []):
            resource = MemosResource(id=res_dto.get("id"), type=res_dto.get("type"))
            resources.append(resource)
        return MemosContent(
            creator_username=dto.get("creatorUsername"),
            content=dto.get("content"),
            resources=resources
        )
