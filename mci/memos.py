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
            content=dto.get("content"),
            resources=resources
        )

    def get_image_resource(self):
        for resource in self.resources:
            if resource.type.startswith("image"):
                return resource

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MemosMinecraftDto:
    post_url: str
    image_url: str
    creator_username: str
    content: str

def get_memos_image(token: str, memo_id: int) -> MemosMinecraftDto:
    memos_content = _get_memos_content(token, memo_id)
    memos_image_resource = memos_content.get_image_resource()
    if memos_image_resource:
        return MemosMinecraftDto(
            post_url=f"{memos_public_url}/m/{memos_content.id}",
            image_url=f"{memos_public_url}/o/r/{memos_image_resource.id}",
            creator_username=memos_content.creator_username,
            content=memos_content.content
        )


def _get_memos_content(token: str, memo_id: int) -> MemosContent:
    response = requests.get(f"{memos_url}/api/v1/memo/{memo_id}", headers=_build_headers(token))
    return MemosContent.from_dto(response.json())


def _build_headers(token: str):
    return {
        "Authorization": "Bearer " + token
    }


