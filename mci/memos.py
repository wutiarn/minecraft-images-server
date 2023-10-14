from dataclasses import dataclass

import requests
from dataclasses_json import dataclass_json, LetterCase

from mci.config import memos_url, memos_public_url


@dataclass
class MemosResource:
    id: int
    type: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MemosContent:
    id: str
    creator_username: str
    created_at: int
    content: str
    resources: list[MemosResource]

    @staticmethod
    def from_dto(dto: dict):
        resources = []
        for res_dto in dto.get("resourceList", []):
            resource = MemosResource(id=res_dto.get("id"), type=res_dto.get("type"))
            resources.append(resource)
        return MemosContent(
            id=dto.get("id"),
            creator_username=dto.get("creatorUsername"),
            created_at=dto.get("createdTs"),
            content=dto.get("content"),
            resources=resources
        )

    def get_image_resource(self):
        for resource in self.resources:
            if resource.type.startswith("image"):
                return resource

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MemosMinecraftMetadata:
    id: str
    url: str
    created_at: int
    description: str

def get_memos_metadata(token: str, memo_id: int) -> MemosMinecraftMetadata:
    memos_content = _get_memos_content(token, memo_id)
    return MemosMinecraftMetadata(
        id=memos_content.id,
        url=f"{memos_public_url}/m/{memos_content.id}",
        created_at=memos_content.created_at,
        description=memos_content.content
    )


def _get_memos_content(token: str, memo_id: int) -> MemosContent:
    response = requests.get(f"{memos_url}/api/v1/memo/{memo_id}", headers=_build_headers(token))
    return MemosContent.from_dto(response.json())


def _build_headers(token: str):
    return {
        "Authorization": "Bearer " + token
    }


