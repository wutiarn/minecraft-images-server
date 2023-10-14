import logging
from dataclasses import dataclass

import requests
from dataclasses_json import dataclass_json, LetterCase
from flask import abort

from mci.config import memos_url, memos_public_url

logger = logging.getLogger("memos")

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
    updated_at: int
    content: str
    resources: list[MemosResource]

    @staticmethod
    def from_dto(dto: dict):
        resources = []
        if type(dto) is list:
            dto = dto[0]
        for res_dto in dto.get("resourceList", []):
            resource = MemosResource(id=res_dto.get("id"), type=res_dto.get("type"))
            resources.append(resource)
        return MemosContent(
            id=dto.get("id"),
            creator_username=dto.get("creatorUsername"),
            created_at=dto.get("createdTs"),
            updated_at=dto.get("updatedTs"),
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
    updated_at: int
    description: str

def get_memos_minecraft_metadata(token: str, memo_id: int) -> MemosMinecraftMetadata:
    memos_content = get_memos_content(token, memo_id)
    return MemosMinecraftMetadata(
        id=memos_content.id,
        url=f"{memos_public_url}/m/{memos_content.id}",
        created_at=memos_content.created_at,
        updated_at=memos_content.updated_at,
        description=memos_content.content
    )


def get_memos_content(token: str, memo_id: int) -> MemosContent:
    if memo_id:
        response = requests.get(f"{memos_url}/api/v1/memo/{memo_id}", headers=_build_headers(token))
    else:
        response = requests.get(f"{memos_url}/api/v1/memo?limit=1", headers=_build_headers(token))
    _handle_memo_error(response)
    return MemosContent.from_dto(response.json())

def get_resource(token: str, resource_id: int):
    return requests.get(f"{memos_url}/o/r/{resource_id}", headers=_build_headers(token))

def _handle_memo_error(response):
    if response.status_code != 200:
        response_text = response.text
        logger.error(f"Received error from memos. Url: {response.url}. Status: {response.status_code}. Body: {response_text}")
        abort(response.status_code, "Received error from memo: " + response_text)


def _build_headers(token: str):
    return {
        "Authorization": "Bearer " + token
    }


